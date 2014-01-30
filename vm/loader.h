
#ifndef __LOADER_H___
#define __LOADER_H___

#include <stdio.h>
#include "mvm.h"

typedef struct Loader TLoader;

struct Loader {
    FILE* fStream;
    TInst* fCode;
    int fCodeLen;
};

TLoader* Loader_New(void);
int TLoader_Load(TLoader* self, const char* filename);
void TLoader_Delete(TLoader* self);


#endif
