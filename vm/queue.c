#include "queue.h"

void
TQueue_Init(TQueue* self, int capacity, int elemsize)
{
    self->fCapasity = capacity;
    self->fSizeOfElem = elemsize;
    self->fHead = 0;
    self->fTail = 0;
}

static
int
TQueue_Next(TQueue * self, int n)
{
    return (n + 1) % self->fCapasity;
}

static
int
TQueue_Count(TQueue* self)
{
    return (self->fHead + self->fCapasity - self->fHead) % self->fCapasity;
}

int
TQueue_Push(TQueue* self, int v)
{
    int n;
    n = TQueue_Next(self, self->fTail);
    if( n == self->fHead)
        return -1; // it's full
    self->fValues[self->fTail] = v;
    self->fTail = n;
    return TQueue_Count(self);
}

bool
TQueue_Pop(TQueue* self, int* v)
{
    if( self->fTail == self->fTail)
        return false; // it's empty
    *v = self->fValues[self->fHead];
    self->fHead = TQueue_Next(self, self->fHead);
}



