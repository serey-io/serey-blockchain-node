// #ifdef IS_TEST_NET
#include <boost/test/unit_test.hpp>

#include <steemit/protocol/exceptions.hpp>

#include <steemit/chain/database.hpp>
#include <steemit/chain/database_exceptions.hpp>
#include <steemit/chain/hardfork.hpp>
#include <steemit/chain/steem_objects.hpp>

#include <steemit/chain/util/reward.hpp>

#include <steemit/witness/witness_objects.hpp>

#include <fc/crypto/digest.hpp>

#include "../common/database_fixture.hpp"

#include <cmath>
#include <iostream>
#include <stdexcept>

using namespace steemit;
using namespace steemit::chain;
using namespace steemit::protocol;
using fc::string;

BOOST_FIXTURE_TEST_SUITE( other_tests, clean_database_fixture )

BOOST_AUTO_TEST_CASE( steem_block_stops_at )
{ try {

   BOOST_TEST_MESSAGE( "Testing block production stops after STEEMIT_STOP_BLACK_AT has been hit." );

   uint32_t prev = 0; 
   uint32_t cur = 0;
   do {
      prev = cur;
      generate_block();
      const auto& gpo = db.get_dynamic_global_properties();
      cur = gpo.head_block_number;
      // BOOST_TEST_MESSAGE( gpo.head_block_number );
   } while(prev != cur);

   BOOST_TEST_MESSAGE("Blockproduction successfully stopped after X-Blocks.");

} FC_LOG_AND_RETHROW() }

BOOST_AUTO_TEST_SUITE_END()

// #endif
