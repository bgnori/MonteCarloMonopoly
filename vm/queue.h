
#include <stdbool.h>

typedef struct {
    int fCapasity;
    int fSizeOfElem;
    int fHead;
    int fTail;
    int fValues[];
} TQueue;

void TQueue_Init(TQueue* self, int capacity, int elemsize);
int TQueue_Push(TQueue* self, int v);
bool TQueue_Pop(TQueue* self, int *v);

