#include <stdlib.h>
#include <assert.h>

#include "loader.h"


TLoader* 
Loader_New()
{
    TLoader* p;

    p = malloc(sizeof(TLoader));
    if(!p)
        return NULL;
    p->fStream = NULL;
    p->fCode = NULL;
    p->fCodeLen = -1;
    return p;
}


int
TLoader_Load(TLoader* self, const char* filename)
{
    int len;

    self->fStream = fopen(filename, "r");
    if(!self->fStream){
        return -1;
    }
    fseek(self->fStream, 0, SEEK_END);
    len = ftell(self->fStream);
    rewind(self->fStream);

    if(len < 0|| len%sizeof(TInst)){ goto free_stream; }

    if (len == 0){
        self->fCode = NULL;
        self->fCodeLen = 0;
        return 0;
    }

    self->fCode = malloc(len);
    if(!self->fCode){
        goto free_stream;
    }
    fread(self->fCode, sizeof(TInst), len/sizeof(TInst), self->fStream);
    self->fCodeLen = len/sizeof(TInst);
    return self->fCodeLen;


free_stream:
    fclose(self->fStream);
    self->fCode = NULL;
    self->fCodeLen = -1;
    return -1;
}


void
TLoader_Delete(TLoader* self)
{
    if (self->fStream)
        fclose(self->fStream);
    if (self->fCode)
        free(self->fCode);
    return;
}


