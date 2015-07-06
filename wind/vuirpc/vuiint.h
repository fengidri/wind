/**
 *   author       :   丁雪峰
 *   time         :   2014-09-02 17:59:22
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.1
 *   description  :   
 */
#ifndef  __VUIINT_H__
#define __VUIINT_H__
#define API
#define INER static

void start_quick_search();
API void set_code(int code, char *reason);
API void send_replay(const char *rep);
API void set_infos(cJSON *json);

#endif


