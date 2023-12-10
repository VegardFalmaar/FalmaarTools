#include <iostream>
#include <iomanip>

#include "ft.hpp"


bool test_string_split()
{
  using namespace std;
  using namespace ft::string;

  if (split("Hello World!", ' ') != vector<string>{"Hello", "World!"})
    return false;

  if (split("Hello,World,how,go,there", ',') != vector<string>{"Hello", "World", "how", "go", "there"})
    return false;

  return true;
}


bool test_string_strip()
{
  if (ft::string::strip("   Hello ", ' ') != "Hello")
    return false;

  if (ft::string::strip("Hello\n", '\n') != "Hello")
    return false;

  if (ft::string::strip("xHello ", 'x') != "Hello ")
    return false;

  return true;
}


typedef bool (*test_func_t) ();
typedef struct {
  test_func_t function;
  char const *name;
} test_func_info_t;


bool run_tests () {
  using namespace std;

  bool test_passed;
  bool tests_passed = true;

  #define init_test_arr(NAME) test_func_info_t {NAME, #NAME}
  test_func_info_t test_funcs[] {
    init_test_arr(test_string_split),
    init_test_arr(test_string_strip),
  };
  const int num_tests = sizeof(test_funcs) / sizeof(test_func_info_t);

  cout << "\nRunning " << num_tests << " test(s):\n\n" << left << setfill ('.');
  for (int i=0; i<num_tests; i++) {
    cout << setw (60) << test_funcs[i].name;
    test_passed = test_funcs[i].function();
    tests_passed = (tests_passed && test_passed);
    if (test_passed)
      cout << " passed\n";
    else
      cout << " failed x\n";
  }

  if (tests_passed)
    std::cout << "\nSuccess!" << std::endl;
  else
    std::cout << "\nFailed!" << std::endl;

  return tests_passed;
}


int main ()
{
  run_tests();

  return 0;
}
