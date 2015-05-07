/**
 *   author       :   丁雪峰
 *   time         :   2014-10-18 09:56:18
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.2
 *   description  :   用于判断patten在string中是否存在并返回相关的信息.
 *
 *   patten形如: 如: BB cc Aa Dd.  由空格分开多个subpatten. 
 *
 *   程序主要分析subpatten 在string 中是否存在与并返回所在的位置.
 *
 *   存在的定义: 这里的字符比较是不同于strstr. subpatten中的小字字母可以匹配大小
 *   写字母. 但是其中的大写字母只能匹配大写字母.
 *
 *   返回结果: 是多个substring. 这些substring 的顺序与在string 中的顺序是相同的. 
 *
 *   对于string与patten 的使用, 程序都没有进行字符串的复制. 都是使用指针直接引用
 *   的.
 *
 *   当subpatten中有一个不能在string 中找到的情况程序会返回false. 如果subpatten
 *   在string 中的顺序与在patten 中的顺序是相同的时候, 当然如你所愿. 但是当不同
 *   的时候会首先在当前已经分析完并拆分成多段substring中的最后一个substring 中
 *   进行查找. 如果没有找到会历遍所的substring 进行查找. 但是会路过已经match 的
 *   substring. 也就说如果string 中只有一个AA. 但是subpatten 中有两个aa. 这时会
 *   被认定为匹配失败.
 *
 *  1.0.2
 *       完成1.0.1的TODO:
 *        1. 把对于patten 的分析与字符匹配进行分开. 因为可能会在很多场景下使用一
 *        个patten 对于许多string 进行分析.
 *
 *        2. 返回结果使用链表的情形. 目前使用数组的结构, 当向中间进行插入数据的
 *        时候必须使用memmove这会很慢. 并且数据的使用中并不方便.
 */
#include <stdio.h>
#include <stddef.h>
#include <unistd.h>
#include <stdbool.h>
#include <malloc.h>
#include <string.h>

#include "so.h"


/**
 * strstrcase -- 在src 中查找pat. 如说明中说过的那样. 小写字母可以匹配大小写.
 *               大写字母只能匹配大写字母.
 * @src: 
 * @len: 
 * @pat: 
 * @size: 
 */
static const char * strstrcase(const char *src, size_t len, 
        const char *pat, size_t size)
{

    size_t offset;
    size_t f;
    int tmp;
    const char *p;
    if (len < size) return NULL;
    f = 0;
    do{
        p = pat;
        offset = 0;
        do{
            tmp = *p - *(src + offset + f);
            if(0 != tmp && 32 != tmp) break;
            ++offset;
            ++p;
            if (offset >= size) return src  + f;
        }while(1);
        ++f;
    }while(f <= len - size);
    return NULL;
}




/**
 * skipspace -- 返回从pos位置开始, 第一个非空格的字符的指针. 可以是当前字符
 * @pos: 指向字符串
 */
static inline const char *skipspace(const char *pos)
{
    while(' ' == *pos) pos++; 
    return 0 == *pos ? NULL : pos;
}

/**
 * skipchar -- 要求当前指向一个字符
 * @pos: 
 */
static inline const char *skipchar(const char *pos)
{
    while(' ' != *pos && 0 != *pos) pos++; 
    return pos;
}


/**
 * nextword -- 要求当前指向一个字符
 * @pos: 
 */
static inline const char *nextword(const char *pos)
{
    return skipspace(skipchar(pos));
}

static inline int countword(const char *pos)
{
    int index = 0;
    pos = skipspace(pos);
    while(pos)
    {
        ++ index;
        pos = nextword(pos);
    }
    return index;
}




/**
 * matched_new -- 在so_matched链表中增加新的节点
 * @set: 
 * @m: 
 */
static struct so_matched *matched_new(struct so_setmatched *set, struct so_matched *m)
{
    struct so_matched *newm, *t;
    newm = set->mmem + set->size;
    ++set->size;

    t = m->next;
    m->next = newm;
    newm->next = t;

    if (NULL == newm->next) set->mtail = newm;

    return newm;
}


/**
 * match_init -- 使用string 初始set. 之后才可以使用find_match
 * @string: 
 * @set: 
 */
static void match_init(const char *string, struct so_setmatched *set)
{
    set->next = set->mtail = set->mmem;
    set->next->s = string;
    set->next->len = strlen(string);
    set->next->match = false;
    set->next->next = NULL;
    set->size = 1;
}


/**
 * find_match -- 
 * @set: 
 * @start: 
 * @end: 
 *      首先比较最后一个elems 的match是不是true, 如果不就从这个elems 中进行比较.
 *      否则或比较失败就从 
 */
static bool find_match(struct so_setmatched * set, const struct so_pat *pat)
{
    const char *target;
    struct so_matched *elem, *elem1, *elem2;

    elem = set->mtail;//首先检查链表尾
    if (!elem->match)
    {
        target = strstrcase(elem->s, elem->len, pat->p, pat->len);

        if (target) goto success;
        else goto loop;
    }
loop:
    elem = set->next;
    while(elem)
    {
        if (!(elem->match || elem == set->mtail)){
            // 跳过match与最后一个
            target = strstrcase(elem->s, elem->len, pat->p, pat->len);
            if (target) goto success;
        }

        elem = elem->next;
    }
    return false;
success:
    if (pat->len == elem->len)// 全等
    {
        elem->match = true;
        elem->p = pat;
    }
    else if (target == elem->s)// 头对齐
    {
        elem1 = matched_new(set, elem);

        elem1->match = false;
        elem1->len = elem->len - pat->len;
        elem1->s = elem->s + pat->len;

        elem->match = true;
        elem->p = pat;
        elem->len = pat->len;

    }
    else if (target + pat->len == elem->s + elem->len)//尾对齐
    {
        elem1 = matched_new(set, elem);

        elem1->match = true;
        elem1->len = pat->len;
        elem1->s = target;
        elem1->p = pat;

        elem->len -= pat->len;
    }
    else if(target > elem->s && target + pat->len < elem->s + elem->len){// 三断
        elem1 = matched_new(set, elem);

        elem1->match = true;
        elem1->len = pat->len;
        elem1->s = target;
        elem1->p = pat;


        elem2 = matched_new(set, elem1);

        elem2->match = false;
        elem2->len = elem->len - pat->len - (target -  elem->s) ;
        elem2->s = target + pat->len;

        elem->len = target -  elem->s;
    }
    else{
        return false;
    }
    return true;

}
/**
 * analy_patten -- 对于patten 进行分析, 构造so_setmatched 数据结构
 * @patten: 
 * 当subpatten 的数量是0 时, 返回NULL; 结果是动态内存, 注意释放
 */
struct so_setmatched *so_compile_patten(const char *patten)
{
    struct so_setmatched *set;// 用于保存返回结果
    struct so_pat *subpat;
    const char *pos, *start, *end;
    int index;
    int total;

    index = countword(patten);// 返回patten 中的key 数量
    if (0 == index) return NULL;

    total = index * 2 + 1;
    set = (struct so_setmatched *)malloc(
            sizeof(struct so_setmatched) + 
            sizeof(struct so_pat) * index + 
            sizeof(struct so_matched) * total);

    set->mtotle = total;
    set->ptotle = index;
    set->size = 1;

    //注意这里的next与mtail 并没有初始化数据内容. 在使用match_find 之前要初始化
    set->mmem = (struct so_matched *)(
            (char *)set + 
            sizeof(struct so_setmatched) + 
            sizeof(struct so_pat) * index);
    set->mtail = set->next = set->mmem;

    subpat = set->subpats;
    pos = skipspace(patten);
    while(pos){
        start = pos;
        end = skipchar(pos);

        subpat->p = start;
        subpat->len = end - start;
        ++subpat;

        pos = skipspace(end);
    }
    return set;
}

bool so_subsearchs(const char *string, struct so_setmatched *set)
{
    size_t i;
    match_init(string, set);

    for (i=0; i < set->ptotle; ++i)
    {
        if(!find_match(set,  set->subpats + i)) return false;
    }
    return true;
}

/**
 * match_key -- 依据patten 在string 中查找合符的子字符
 * @string:   源字符串
 * @patten:   模式
 * @res:      OUT 用于返回结果
 * @m:        IN res 的大小 OUT 实际的大小.
 */
bool so_subsearch(const char *string, const char *patten, 
        struct so_setmatched **res)
{
    struct so_setmatched *set;
    set = so_compile_patten(patten);
    if (!set) return false;

    if (!so_subsearchs(string, set))
    {
        free(set);
        return false;
    }
    *res = set;
    return true;
}

#if TEST
int main(int argn, char *argv[])
{
    struct so_setmatched *set;
    struct so_matched *elem;
    const char *string;
    const char *patten;
    unsigned int i; 
    bool r;

    string = argv[1];
    patten = argv[2];
    r = so_subsearch(string, patten, &set);
    printf("string: %s\n", string);
    printf("patten: %s\n", patten);
    if (!r)
    {
        printf("match fiald\n");
        return -1;
    }
    printf("mtotal:%zu size:%zu ptotal:%zu\n", set->mtotle, 
            set->size, set->ptotle);

    elem = set->next;
    while(elem)
    {
        printf("%d:%d \t |%.*s|\n", elem->match,
                (int)elem->len ,
                (int)elem->len ,
                elem->s);
        elem = elem->next;

    }
    free(set);


}
#endif

