#ifndef __UNITTEST_H__
#define __UNITTEST_H__

typedef const char* const_char_p;
typedef struct TestContext TTestContext;

typedef const_char_p (*TestCase)(TTestContext* ctx);
typedef int (*TFailProc)(TTestContext* ctx);

int test_runner(TTestContext* ctx, const TestCase* cases, int count);

struct TestContext {
    TFailProc fOnFail;
};

#endif

