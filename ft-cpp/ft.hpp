#ifndef __FT_HPP
#define __FT_HPP

#include <string>
#include <vector>
#include <sstream>

namespace ft::string
{
  std::vector<std::string> split(const std::string s, const char c)
  {
    std::stringstream ss(s);
    std::string substring;
    std::vector<std::string> result;
    while (getline(ss, substring, c))
      result.push_back(substring);
    return result;
  }

  std::string strip(const std::string s, const char c)
  {
    size_t start = 0;
    while (s[start] == c)
      ++start;
    size_t len = s.size() - start;
    while (s[start + len - 1] == c)
      --len;
    return s.substr(start, len);
  }

  // std::string replace(const std::string, const std::string);
}

#endif
