
#include <stdbool.h>
#include <stdint.h>

#define QSIZE 20

typedef int32_t elemT;

typedef struct {
    int fHead;
    int fTail;
    int fValues[QSIZE];
} TQueue;

void TQueue_Init(TQueue* self);
int TQueue_Push(TQueue* self, int v);
bool TQueue_Pop(TQueue* self, int *v);

