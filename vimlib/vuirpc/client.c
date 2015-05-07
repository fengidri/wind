/**
 *   author       :   丁雪峰
 *   time         :   2014-08-30 10:04:45
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.1
 *   description  :
 */
#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#define REQUEST_POST "POST"

#include "rnetwork/zmalloc.h"
#include "rnetwork/anet.h"
#include "rnetwork/ae.h"
#include "rlist/adlist.h"
#include "rstr/sds.h"
#include "cJSON/cJSON.h"


#include "vuirpc.h"
#include "client.h"

void setResCode(vuiClient *c, int code, char *reason);
void addReplay(vuiClient *c, const char *body);
typedef void (*vuicallback)(vuiClient *c, cJSON *jon);
struct callback{
    const char * url;
    vuicallback fun;
};

void process_local_tag(vuiClient *c, cJSON *jon);

struct callback vuicallbacks[20] = {
    {"/localtag", process_local_tag}
};



int csplit(char *src, char dim, char **res, int nm)
{
    char *c;
    int count;
    int flag;

    flag = count = 0;
    c = src;
    while(*c)
    {
        if (*c == dim)
        {
            flag = *c = 0;
        }
        else{
            if(!flag){
                if (count < nm)
                {
                    *res = c;
                    res++;
                }
                count ++;
                flag = 1;
            }
        }
        c++;
    }
    return count;
}
const char *skipspace(const char *buf)
{
    const char *c;
    c = buf;

    while(*c)
    {
        if(' ' != *c)
        {
            return c;
        }
        c++;
    }
    return NULL;
}
const char *skiptospace(const char *buf)
{
    const char *c;
    c = buf;
    while(*c)
    {
        if(' ' == *c)
        {
            return c;
        }
        c++;
    }
    return NULL;
}
void processRequest(vuiClient *c)
{
    if (c->procing != PROC_END)
    {
        setResCode(c, 502, "Procing");
        addReplay(c, NULL);
        return;
    }
    c->procing = PROC_ING;
    cJSON *root = cJSON_Parse(c->prot.body);
    if (!root)
    {
        setResCode(c, 501, "Json format error");
        addReplay(c, "");
        return;
    }
    if (!listAddNodeTail(c->jsons, root))
    {
        cJSON_Delete(root);
        setResCode(c, 502, "Save Jsons fail!");
        addReplay(c, "");
        return;
    }
    process_local_tag(c, root);

}
int resolveHeader(sds buf, struct request *prot)
{
    char *n;
    char *t;
    char *tmp[3];
    n = strstr(buf, "\r\n");
    *n = 0;
    n += 2;
    prot->waiting = 0;
    if (sizeof(tmp)/sizeof(char *) != 
            csplit(buf, ' ', tmp, sizeof(tmp)/sizeof(char *)))
    {
        return -1;
    }

    prot->method  = tmp[0];
    prot->url     = tmp[1];
    prot->version = tmp[2];

    t = strstr(n, "length:");
    if (NULL == t)  return  -1;//error 

    t = (char *)skiptospace(t);
    if (NULL == t)  return  -1;//error 

    t = (char *)skipspace(t);
    if (NULL == t)  return  -1;//error 

    prot->lenght = atoi(t);
    prot->hlenght = sdslen(buf);
    return 0;
}
int resloveMessage(char **msg, vuiClient *c)
{
    char *buf;
    char *body;
    int left;
    buf = *msg;


    body = strstr(buf, "\r\n\r\n");
    if (NULL == body)return -2;//continue read //头部没有结束 
    body = body + 4; 
    c->querymsg = sdscpylen(c->querymsg, buf, body - buf);

    if (0 != resolveHeader(c->querymsg, &c->prot)){
        *msg = body;
        return -1;
    }
    left = sdslen(c->querybuf) - (body - c->querybuf);
    if (c->prot.lenght <= left)
    {
        c->querymsg = sdscatlen(c->querymsg, body, c->prot.lenght);
        *msg = body + c->prot.lenght;
        return 0;
    }
    c->prot.waiting = c->prot.lenght - left;
    c->querymsg = sdscat(c->querymsg, body);
    return -3;
}
void  processInputBuffer(vuiClient *c)
{
    int res;
    char *buf;
    int len;

    buf = c->querybuf;
    len = sdslen(c->querybuf);

    if (c->prot.waiting)
    {
        if (len >= c->prot.waiting)
        {
            c->querymsg = sdscatlen(c->querymsg, buf, c->prot.waiting);
            buf += c->prot.waiting;
            c->prot.waiting = 0;
            goto deal;
        }
        else
        {
            c->querymsg = sdscatlen(c->querymsg, buf, len);
            c->prot.waiting -= len;
            goto clear;
        }
    }

    while((buf = strstr(buf, REQUEST_POST " ")))//找报文头
    {
        res = resloveMessage(&buf, c);
        switch(res)
        {
            case -3:
                goto clear;
            case -2://contiune read
                if (buf != c->querybuf)
                {
                    sdsrange(c->querybuf, buf - c->querybuf, -1);
                }
                goto res;
            case 0:
deal:
                c->prot.body = c->querymsg + c->prot.hlenght;
                processRequest(c);
            case -1:
                break;
        }
    }
clear:
    sdsclear(c->querybuf);
res:
    return;
}


void sendReplay(aeEventLoop *el, int fd, void *privdata, int mask)
{
    vuiClient *c = (vuiClient *)privdata;
    int len;
    int nw;
    char *pos;
    sdsclear(c->res.buf);
    LogInfo("sendReplay....");
    c->res.buf = sdscatprintf(c->res.buf, "%s %d %s\r\nlength: %zu\r\n\r\n%s",
            c->res.version, c->res.code, c->res.reason, 
            sdslen(c->res.body),
            c->res.body);
    len = sdslen(c->res.buf);
    pos = c->res.buf;
    while(len>0)
    {
        nw = write(fd, pos, len);
        pos +=  nw;
        len -= nw;
    }

    //reset
    if (c->res.code >= 200)
    {
        c->procing = PROC_END;
    }
    else{
        c->res.code = 200;
        c->res.reason = sdscpy(c->res.reason, "OK");
        c->procing = PROC_ING;
    }
    aeDeleteFileEvent(el,c->fd,AE_WRITABLE);
}
void addReplay(vuiClient *c, const char *body)
{
    if (body) c->res.body = sdscpy(c->res.body, body);
    else
        sdsclear(c->res.body);
    c->procing = PROC_HALF;
    aeCreateFileEvent(server.el, c->fd, AE_WRITABLE, sendReplay, c);
}


void setResCode(vuiClient *c, int code, char *reason)
{
    c->res.code = code;
    if (!reason) 
    {
        if(code < 200) reason = "Trying";
        else if(code == 200) reason = "OK";
        else if(code == 202) reason = "Accept";
        else if(code <  300) reason = "Created";
        else if(code <  400) reason = "Keep";
        else if(code == 404) reason = "Not Found";
        else if(code <  500) reason = "Error";
        else if(code <  600) reason = "Error";
        else reason = "Error";
    }
    c->res.reason = sdscpy(c->res.reason, reason);
}

void readQueryFromClient(aeEventLoop *el, int fd, void *privdata, int mask) {
    vuiClient *c = (vuiClient *) privdata;
    int nread, readlen;
    size_t qblen;

    /* If this is a multi bulk request, and we are processing a bulk reply
     * that is large enough, try to maximize the probability that the query
     * buffer contains exactly the SDS string representing the object, even
     * at the risk of requiring more read(2) calls. This way the function
     * processMultiBulkBuffer() can avoid copying buffers to create the
     * Redis Object representing the argument. */
    if (c->prot.waiting)
    {
        readlen = c->prot.waiting;
    }
    else
    {
        readlen = 1024 * 2;
    }

    qblen = sdslen(c->querybuf);
    c->querybuf = sdsMakeRoomFor(c->querybuf, readlen);
    nread = read(fd, c->querybuf+qblen, readlen);

    if (nread == -1) {
        if (errno == EAGAIN) {
            nread = 0;
        } else {
            LogInfo("Reading from client: %s",strerror(errno));
            freeClient(c);
            return;
        }
    } else if (nread == 0) {
        LogInfo("Client closed connection");
        freeClient(c);
        return;
    }
    if (nread) {
        sdsIncrLen(c->querybuf,nread);
    } 
    //TODO
    if (sdslen(c->querybuf) > 1024 * 1024) {
        LogWarn("Closing client that reached max query buffer length");
        sdsclear(c->querybuf);
        freeClient(c);
        return;
    }
    processInputBuffer(c);
}


vuiClient * createClient(int fd)
{
    if (server.client != NULL)
    {
        close(fd);
        return NULL;
    }
    LogInfo("creat client fd:%d", fd);
    vuiClient *c = zmalloc(sizeof(vuiClient));
    memset(c, 0, sizeof(vuiClient));

    c->querybuf = sdsempty();
    c->querymsg = sdsempty();

    c->prot.method = NULL;
    c->prot.version = NULL;
    c->prot.body = NULL;
    c->prot.lenght = 0;
    c->prot.waiting = 0;

    c->res.version = "VPC/1.0";
    c->res.code = 200;
    c->res.reason = sdsnew("OK");
    c->res.body = sdsempty();
    c->res.buf = sdsempty();

    c->jsons = listCreate();

    c->fd = fd;


    anetNonBlock(NULL,fd);
    anetEnableTcpNoDelay(NULL,fd);
    if (aeCreateFileEvent(server.el, fd, AE_READABLE,
                readQueryFromClient, c) == AE_ERR)
    {
        close(fd);
        zfree(c);
        return NULL;
    }
    server.client = c;
    return c;

}


void freeClient(vuiClient *c) {
    listNode *ln;
    listIter *it;
    cJSON *json;

    /* Free the query buffer */
    sdsfree(c->querybuf);
    sdsfree(c->querymsg);
    sdsfree(c->res.body);
    sdsfree(c->res.reason);
    sdsfree(c->res.buf);

    /* Close socket, unregister events, and remove list of replies and
     * accumulated arguments. */
    if (c->fd != -1) {
        aeDeleteFileEvent(server.el,c->fd,AE_READABLE);
        aeDeleteFileEvent(server.el,c->fd,AE_WRITABLE);
        close(c->fd);
    }
    it = listGetIterator(c->jsons, AL_START_HEAD);

    while((ln = listNext(it)))
    {
        json = (cJSON *)ln->value;
        cJSON_Delete(json);
        listDelNode(c->jsons, ln);
    }
    listRelease(c->jsons);
    listReleaseIterator(it);


    zfree(c);
    server.client = NULL;
}
