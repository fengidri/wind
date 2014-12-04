/**
 *   author       :   丁雪峰
 *   time         :   2014-08-30 09:15:27
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.1
 *   description  :
 */
#include "rnetwork/ae.h"
#include "rnetwork/anet.h"
#include "vuirpc.h"
#include "client.h"
#include "rlist/adlist.h"
void acceptTcpHandler(aeEventLoop *el, int fd, void *privdata, int mask) {
    int cport, cfd;
    char cip[ADDR_IP_LEN];
    char neterr[ANET_ERR_LEN];
    vuiClient *client;

    cfd = anetTcpAccept(neterr, fd, cip, sizeof(cip), &cport);
    if (cfd == AE_ERR) {
        LogWarn("Accepting client connection: %s", neterr);
        return;
    }
    LogWarn("Accepted %s:%d", cip, cport);
    client = createClient(cfd);
    if (client == NULL)
    {
        LogWarn("just support one client one time");
    }
}

