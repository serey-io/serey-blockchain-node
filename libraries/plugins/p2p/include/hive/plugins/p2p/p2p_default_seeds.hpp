#pragma once

#include <vector>

namespace hive{ namespace plugins { namespace p2p {

#ifdef IS_TEST_NET
const std::vector< std::string > default_seeds;
#else
const std::vector< std::string > default_seeds = {
  //"seed-v2.serey.io:2001"
};
#endif

} } } // hive::plugins::p2p
