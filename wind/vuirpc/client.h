/**
 *   author       :   丁雪峰
 *   time         :   2014-08-30 10:06:56
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.1
 *   description  :   
 */
#include "rstr/sds.h"
#include "rlist/adlist.h"
#ifndef  __CLIENT_H__
#define __CLIENT_H__
#define PROC_ING  2
#define PROC_HALF 1
#define PROC_END  0

struct request{
    const char *method;
    const char *url;
    const char *version;
    int hlenght;
    int lenght;
    char *body;
    int waiting;
};

struct response{
    const char *version;
    int   code;
    sds   reason;
    int   lenght;
    sds   body;
    sds   buf;
};

typedef struct vuiClient {
    int fd;
    struct request prot;
    struct response res;


    sds querybuf;
    sds querymsg;
    int procing;
    list *jsons;

} vuiClient;
void freeClient(vuiClient *c);
vuiClient * createClient(int fd);

void addReplay(vuiClient *c, const char *body);
void setResCode(vuiClient *c, int code, char *reason);

#endif


