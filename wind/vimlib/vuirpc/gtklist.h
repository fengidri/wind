/**
 *   author       :   丁雪峰
 *   time         :   2014-09-13 17:17:14
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.1
 *   description  :   
 */
#ifndef  __GTKLIST_H__
#define __GTKLIST_H__
void list_selnext(GtkWidget *w);
void list_selpre(GtkWidget *w);
void list_append(GtkWidget *list, const gchar *str, const gchar *value);
void list_clear(GtkWidget *list);
void list_select(GtkWidget *list, int index);
int list_selected(GtkWidget *list, int column, GValue *buf);

#endif


