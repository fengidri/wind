/**
 *   author       :   丁雪峰
 *   time         :   2014-08-30 09:39:32
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.1
 *   description  :   
 */
#ifndef  __VUIRPC_H__
#define __VUIRPC_H__
#include <stdio.h>
#define LogError(fmt, ...) printf(fmt "\n", ## __VA_ARGS__)
#define LogWarn(fmt, ...) printf(fmt "\n", ## __VA_ARGS__)
#define LogInfo(fmt, ...) printf(fmt "\n", ## __VA_ARGS__)
#define ADDR_IP_LEN  40

#include "rnetwork/ae.h"
#include "rlist/adlist.h"
#include "client.h"

struct _server{
    int fd;
    aeEventLoop *el;
    int backlog;
    char neterr[256];
    const char *host;
    int port;
    vuiClient *client;
};

extern  struct _server server;

#endif


