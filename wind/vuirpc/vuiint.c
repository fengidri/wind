/**
 *   author       :   丁雪峰
 *   time         :   2014-09-02 17:58:33
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.1
 *   description  :
 */
#include <stdio.h>
#include <stddef.h>
#include <unistd.h>
#include <pthread.h>

#include "quick_search.h"
#include "client.h"
#include "vuiint.h"
#include "vuirpc.h"
#include "cJSON/cJSON.h"





INER void *__start_quick_search(void *arg)
{
    quick_search();

    if (server.client && server.client->procing == PROC_ING)
    {
        set_code(509, "Error");
        send_replay("");
    }
    return NULL;
}
API void set_infos(cJSON *json)
{
    qs_set_infos(json);
}

API void send_replay(const char *rep)
{
    if (server.client)
        addReplay(server.client, rep);
}

API void set_code(int code, char *reason)
{
    if (server.client)
        setResCode(server.client, code, reason);
}

API void start_quick_search(vuiClient *c)
{
    pthread_t ntid;
    pthread_create(&ntid, NULL, __start_quick_search, NULL);

}
