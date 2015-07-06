/**
 *   author       :   丁雪峰
 *   time         :   2014-12-03 14:14:50
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.1
 *   description  :   
 */
#ifndef  __SO_H__
#define __SO_H__
#define LOGINFO(fmt, ...)   printf(fmt  "\n", ## __VA_ARGS__)

// 描述subpatten
struct so_pat{
    const char *p;
    size_t len;
};
// 用于描述在 match_key 的返回结果集中的一个元素. 
struct so_matched{
    const char *s;  // substring 
    size_t  len;    // substring的长度, 如果match为真, 则len 与pat 中的相同
    bool match;     // 是否匹配的结果
    const struct so_pat  *p;  // 对应的pat
    struct so_matched *next;
};
struct so_setmatched{
    size_t size;   // substring 的数量
    size_t mtotle;  // substring 的最大容量
    size_t ptotle;  // subpatten 的数量
    struct so_matched *mmem; // 指向保存substring 的连续内存
    struct so_matched *next; // 指向链表的头
    struct so_matched *mtail; // 指向 保存substring 链表的尾
    struct so_pat subpats[];  // subpatten 构成的数组
};

/**
 * analy_patten -- 对于patten 进行分析, 构造so_setmatched 数据结构
 * @patten: 
 * 当subpatten 的数量是0 时, 返回NULL; 结果是动态内存, 注意释放
 */
struct so_setmatched *so_compile_patten(const char *patten);

/**
 * so_subsearchs -- 依赖于已经格式化的set, 查找string 中的substring
 *             set 是由compile_patten函数生成的
 * @string: 
 * @set: 
 */
bool so_subsearchs(const char *string, struct so_setmatched *set);

/**
 * match_key -- 依据patten 在string 中查找合符的子字符
 * @string:   源字符串
 * @patten:   模式
 * @res:      OUT 用于返回结果
 */
bool so_subsearch(const char *string, const char *patten, 
        struct so_setmatched **res);

#endif


