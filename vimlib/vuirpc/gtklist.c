/**
 *   author       :   丁雪峰
 *   time         :   2014-09-13 17:16:27
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.1
 *   description  :
 */
#include <stdio.h>
#include <stddef.h>
#include <unistd.h>

#include <gtk/gtk.h>  

void list_selnext(GtkWidget *w)
{
    GtkTreeSelection *sel;
    GtkTreeModel  *model;
    GtkTreeIter iter;
    sel = gtk_tree_view_get_selection(GTK_TREE_VIEW(w));
    model = gtk_tree_view_get_model(GTK_TREE_VIEW(w));
    if(!gtk_tree_selection_get_selected(sel, &model, &iter))
        return ;
    if(gtk_tree_model_iter_next(model, &iter))
        gtk_tree_selection_select_iter(sel, &iter);

}
void list_selpre(GtkWidget *w)
{
    GtkTreeSelection *sel;
    GtkTreeModel  *model;
    GtkTreeIter iter;
    sel = gtk_tree_view_get_selection(GTK_TREE_VIEW(w));
    model = gtk_tree_view_get_model(GTK_TREE_VIEW(w));
    if(!gtk_tree_selection_get_selected(sel, &model, &iter))
        return ;
    if(gtk_tree_model_iter_previous(model, &iter))
        gtk_tree_selection_select_iter(sel, &iter);

}

void list_append(GtkWidget *list, const gchar *str, const gchar *value)
{
    GtkListStore *store;
    GtkTreeIter iter;

    store = GTK_LIST_STORE(gtk_tree_view_get_model
            (GTK_TREE_VIEW(list)));

    gtk_list_store_append(store, &iter);
    gtk_list_store_set(store, &iter, 0, str, 1, value, -1);
}

void list_clear(GtkWidget *list)
{
  GtkListStore *store;

  store = GTK_LIST_STORE(gtk_tree_view_get_model
      (GTK_TREE_VIEW(list)));

  gtk_list_store_clear(store);

}
void list_select(GtkWidget *list, int index)
{
    GtkTreeSelection *sel;
    GtkListStore *store;
    GtkTreeIter iter;

    sel = gtk_tree_view_get_selection(GTK_TREE_VIEW(list));
    store = GTK_LIST_STORE(gtk_tree_view_get_model
            (GTK_TREE_VIEW(list)));
    if(!gtk_tree_model_get_iter_first(GTK_TREE_MODEL(store), &iter))
        return;
    gtk_tree_selection_select_iter(sel, &iter);
}

int list_selected(GtkWidget *list, int column, GValue *buf)
{
    GtkTreeSelection *sel;
    GtkTreeModel  *model;
    GtkTreeIter iter;
    GtkTreePath *path;

    sel = gtk_tree_view_get_selection(GTK_TREE_VIEW(list));
    model = gtk_tree_view_get_model(GTK_TREE_VIEW(list));
    if(!gtk_tree_selection_get_selected(sel, &model, &iter))
        return -1;
    gtk_tree_model_get_value(model, &iter, column, buf);
    return 0;
}
