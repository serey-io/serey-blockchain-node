#pragma once

#include <steemit/protocol/operation_util.hpp>
#include <steemit/protocol/steem_operations.hpp>
#include <steemit/protocol/steem_virtual_operations.hpp>

namespace steemit { namespace protocol {

   /** NOTE: do not change the order of any operations prior to the virtual operations
    * or it will trigger a hardfork.
    */
   typedef fc::static_variant<
       /*  0 */ vote_operation,
       /*  1 */ comment_operation,

       /*  2 */ transfer_operation,
       /*  3 */ transfer_to_vesting_operation,
       /*  4 */ withdraw_vesting_operation,

       /*  5 */ account_create_operation,
       /*  6 */ account_update_operation,

       /*  7 */ witness_update_operation,
       /*  8 */ account_witness_vote_operation,
       /*  9 */ account_witness_proxy_operation,

       /* 10 */ custom_operation,

       /* 11 */ report_over_production_operation,

       /* 12 */ delete_comment_operation,
       /* 13 */ custom_json_operation,
       /* 14 */ comment_options_operation,
       /* 15 */ set_withdraw_vesting_route_operation,

       /* 16 */ challenge_authority_operation,
       /* 17 */ prove_authority_operation,
       /* 18 */ request_account_recovery_operation,
       /* 19 */ recover_account_operation,
       /* 20 */ change_recovery_account_operation,
       /* 21 */ escrow_transfer_operation,
       /* 22 */ escrow_dispute_operation,
       /* 23 */ escrow_release_operation,
       /* 24 */ escrow_approve_operation,

       /* 25 */ transfer_to_savings_operation,
       /* 26 */ transfer_from_savings_operation,
       /* 27 */ cancel_transfer_from_savings_operation,
       /* 28 */ custom_binary_operation,
       /* 29 */ decline_voting_rights_operation,

       /* 30 */ claim_reward_balance_operation,
       /* 31 */ delegate_vesting_shares_operation,
       /* 32 */ account_create_with_delegation_operation,

            /// virtual operations below this point
       /* 33 */ author_reward_operation,
       /* 34 */ curation_reward_operation,
       /* 35 */ comment_reward_operation,
       /* 36 */ fill_vesting_withdraw_operation,
       /* 37 */ shutdown_witness_operation,
       /* 38 */ fill_transfer_from_savings_operation,
       /* 39 */ hardfork_operation,
       /* 40 */ comment_payout_update_operation,
       /* 41 */ return_vesting_delegation_operation,
       /* 42 */ comment_benefactor_reward_operation,
       /* 43 */ producer_reward_operation
         > operation;

   /*void operation_get_required_authorities( const operation& op,
                                            flat_set<string>& active,
                                            flat_set<string>& owner,
                                            flat_set<string>& posting,
                                            vector<authority>&  other );

   void operation_validate( const operation& op );*/

   bool is_market_operation( const operation& op );

   bool is_virtual_operation( const operation& op );

} } // steemit::protocol

/*namespace fc {
    void to_variant( const steemit::protocol::operation& var,  fc::variant& vo );
    void from_variant( const fc::variant& var,  steemit::protocol::operation& vo );
}*/

DECLARE_OPERATION_TYPE( steemit::protocol::operation )
FC_REFLECT_TYPENAME( steemit::protocol::operation )
