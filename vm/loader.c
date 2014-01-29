#include <stdlib.h>

#include "loader.h"


TLoader* 
Loader_New(const char* filename)
{
    TLoader* p;
    int len;

    p = malloc(sizeof(TLoader));
    p->fStream = fopen(filename, "r");
    p->fCode = NULL;
    p->fCodeLen = 0;

    fseek(p->fStream, 0, SEEK_END);
    len = ftell(p->fStream);
    rewind(p->fStream);

    if(len && !len%sizeof(TInst)){
        fclose(p->fStream);
        free(p);
    }
    
    if(len) {
        p->fCode = malloc(len);
        fread(p, sizeof(TInst), len/sizeof(TInst), p->fStream);
        p->fCodeLen = len/sizeof(TInst);
    }
    return p;
}


void
TLoader_Delete(TLoader* self)
{
    fclose(self->fStream);
    return;
}


