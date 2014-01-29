#include <stdlib.h>
#include <stdio.h>

#include "unittest.h"

bool
_assertEqualInt(int expected, int actual, TTestContext* ctx, const char* msg, const int line, const char* func, const char* filename)
{
    if(expected != actual){
        TTestContext_AddMessage(ctx, msg);
        TTestContext_AddMessage(ctx, func);
        TTestContext_AddMessage(ctx, filename);
        return false;
    }
    return true;
}

bool
_assertNotEqualInt(int expected, int actual, TTestContext* ctx, const char* msg, const int line, const char* func, const char* filename)
{
    if(expected == actual){
        TTestContext_AddMessage(ctx, msg);
        TTestContext_AddMessage(ctx, func);
        TTestContext_AddMessage(ctx, filename);
        return false;
    }
    return true;
}

bool 
_assertNull(void* ptr, TTestContext* ctx, const char* msg, const int line, const char* func, const char* filename)
{
    if(ptr){
        TTestContext_AddMessage(ctx, msg);
        TTestContext_AddMessage(ctx, func);
        TTestContext_AddMessage(ctx, filename);
        return false;
    }
    return true;
}

bool 
_assertNotNull(void* ptr, TTestContext* ctx, const char* msg, const int line, const char* func, const char* filename)
{
    if(!ptr){
        TTestContext_AddMessage(ctx, msg);
        TTestContext_AddMessage(ctx, func);
        TTestContext_AddMessage(ctx, filename);
        return false;
    }
    return true;
}

bool 
TTestContext_Init(TTestContext* self)
{
    self->fMessages = malloc(sizeof(const char*) *  default_message_count); //FIXME
    self->fAlloced = default_message_count;
    self->fUsed = 0;
    return true; //FIXME
}

void
TTestContext_Clean(TTestContext* self)
{
    free(self->fMessages);
}


void
TTestContext_AddMessage(TTestContext* ctx, const char* msg)
{
    printf("TTestContext_AddMessage\n");
    if(ctx->fAlloced == ctx->fUsed){
        ctx->fAlloced *= 2;
        ctx->fMessages = realloc(ctx->fMessages, ctx->fAlloced); //FIXME
    }
    /*
    printf("TTestContext_AddMessage fMessages %p \n", ctx->fMessages);
    printf("TTestContext_AddMessage fAlloced%i \n", ctx->fAlloced);
    printf("TTestContext_AddMessage fUsed%i \n", ctx->fUsed);
    */
    ctx->fMessages[ctx->fUsed] = msg;
    ctx->fUsed +=1;
}

int
test_runner(TTestContext* ctx, const TestCase* cases, int count)
{
    int i, j;
    TestCase t;

    for(i=0; i< count; i++){
        t = cases[i];
        if(!t(ctx)){
            printf("!\n");
            for(j = 0; j < ctx->fUsed; j ++){
                printf("%s\n", ctx->fMessages[j]);
            }
            if (ctx->fOnFail){
                ctx->fOnFail(ctx);
            }
            break;
        }else{
            printf(".");
        }
    }
    return i;
}
