/**
 *   author       :   丁雪峰
 *   time         :   2014-08-30 22:02:35
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.1
 *   description  :
 */
#include <stdio.h>
#include <stddef.h>
#include <unistd.h>

#include "vuirpc.h"
#include "rnetwork/anet.h"
#include "rnetwork/ae.h"
#include "network.h"
#include "rlist/adlist.h"
#include "client.h"
#include "cJSON/cJSON.h"
#include "vuiint.h"
struct _server server;

int main(int argc, char **argv)
{
    server.host = "127.0.0.1";
    server.port = 7878;
    server.backlog = 5;
    server.client = NULL;

    server.fd = anetTcpServer(server.neterr,
            server.port,
            (char *)server.host,
                server.backlog);
    server.el = aeCreateEventLoop(10);
    LogWarn("Start...");
    aeCreateFileEvent(server.el, server.fd, AE_READABLE,
            acceptTcpHandler,NULL);

    aeMain(server.el);
    

}
void process_local_tag(vuiClient *c, cJSON *json)
{
    cJSON *tags  = cJSON_GetObjectItem(json, "values");
    set_infos(tags);
    
    start_quick_search(c);
    setResCode(c, 100, NULL);
    addReplay(c, NULL);

}
