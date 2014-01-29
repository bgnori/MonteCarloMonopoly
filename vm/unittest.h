#ifndef __UNITTEST_H__
#define __UNITTEST_H__

#include <stdbool.h>

typedef struct TestContext TTestContext;

typedef bool (*TestCase)(TTestContext* ctx);
typedef int (*TFailProc)(TTestContext* ctx);

int test_runner(TTestContext* ctx, const TestCase* cases, int count);


bool TTestContext_Init(TTestContext* self);
void TTestContext_Clean(TTestContext* self);

bool _assertEqualInt(int expected, int actual, TTestContext* ctx, const char* msg, const int line, const char* func, const char* filename);
bool _assertNotEqualInt(int expected, int actual, TTestContext* ctx, const char* msg, const int line, const char* func, const char* filename);

bool _assertNull(void* ptr, TTestContext* ctx, const char* msg, const int line, const char* func, const char* filename);
bool _assertNotNull(void* ptr, TTestContext* ctx, const char* msg, const int line, const char* func, const char* filename);

enum {
    default_message_count = 4,
};

void TTestContext_AddMessage(TTestContext* ctx, const char* msg);

struct TestContext {
    const char** fMessages;
    int fAlloced;
    int fUsed;
    TFailProc fOnFail;
};

#define assertNull(ptr, c, m) _assertNull((ptr), (c), (m), __LINE__, __func__, __FILE__)
#define assertNotNull(ptr, c, m) _assertNotNull((ptr), (c), (m), __LINE__, __func__, __FILE__)
#define assertEqualInt(a, b, c, m) _assertEqualInt((a), (b), (c), (m), __LINE__, __func__, __FILE__)
#define assertNotEqualInt(a, b, c, m) _assertNotEqualInt((a), (b), (c), (m), __LINE__, __func__, __FILE__)

#endif

