#include <stdio.h>

#include "loader.h"


TLoader* 
Loader_New(const char* filename)
{
    TLoader* p;
    p = malloc(sizeof(TLoader));
    p->fStream = fopen(filename, "r");
    return p;
}


void
TLoader_Delete(TLoader* self)
{
    fclose(self->fStream);
    return;
}


