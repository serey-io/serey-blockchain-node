#pragma once

#include <steemit/chain/steem_objects.hpp>

#include <steemit/protocol/asset.hpp>
#include <steemit/protocol/config.hpp>
#include <steemit/protocol/types.hpp>

#include <fc/reflect/reflect.hpp>

#include <fc/uint128.hpp>

namespace steemit { namespace chain { namespace util {

using steemit::protocol::asset;
using steemit::protocol::price;
using steemit::protocol::share_type;

using fc::uint128_t;

struct comment_reward_context
{
   share_type rshares;
   uint16_t   reward_weight = 0;
   asset      max_payout;
   uint128_t  total_reward_shares2;
   asset      total_reward_fund_steem;
   curve_id   reward_curve = quadratic;
   uint128_t  content_constant = STEEMIT_CONTENT_CONSTANT_HF0;
};

uint64_t get_rshare_reward( const comment_reward_context& ctx );

inline uint128_t get_content_constant_s()
{
   return STEEMIT_CONTENT_CONSTANT_HF0; // looking good for posters
}

uint128_t evaluate_reward_curve( const uint128_t& rshares, const curve_id& curve = quadratic, const uint128_t& content_constant = STEEMIT_CONTENT_CONSTANT_HF0 );

inline bool is_comment_payout_dust( uint64_t steem_payout )
{
   return asset( steem_payout, STEEM_SYMBOL ) < STEEMIT_MIN_PAYOUT;
}

} } } // steemit::chain::util

FC_REFLECT( steemit::chain::util::comment_reward_context,
   (rshares)
   (reward_weight)
   (max_payout)
   (total_reward_shares2)
   (total_reward_fund_steem)
   (reward_curve)
   (content_constant)
   )
