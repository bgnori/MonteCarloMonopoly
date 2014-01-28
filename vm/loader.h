
#ifndef __LOADER_H___
#define __LOADER_H___

#include <stdio.h>

typedef struct Loader TLoader;

struct Loader {
    FILE* fStream;
};

TLoader* Loader_New(const char* filename);
void TLoader_Delete(TLoader* self);


#endif
