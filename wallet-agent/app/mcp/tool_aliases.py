TOOL_ALIASES = {

    # PROGRAM / CONFIG
    "post_programmanagermgmt_programmanagers": "list_program_managers",
    "post_wallettransferservice_transfertypes": "list_transfer_types",
    "post_customermgmtservice_groups": "list_groups",
    "post_wallettransferservice_systemaccounts": "list_system_accounts",

    # PERSON
    "post_customermgmtservice_getpersondetailsbypersonid": "get_person_by_person_id",
    "post_customermgmtservice_getpersondetailsbymobilenumber": "get_person_by_mobile",
    "post_customermgmtservice_getpersondetailsbycifnumber": "get_person_by_cif",
    "post_customermgmtservice_getpersondetailsbywalletid": "get_person_by_wallet",
    "post_customermgmtservice_getpersondetailsbycustomfield": "get_person_by_custom",
    "post_customermgmtservice_getpersondetailsbybrokerid": "get_person_by_broker",
    "post_customermgmtservice_getpersondetailsbyprogrammanageridandgr": "get_persons_by_group",
    "post_customermgmtservice_getpersonidsbyprogrammanagerid": "list_person_ids",
    "post_customermgmtservice_getcountofregisteredpersons": "count_registered_persons",

    # PERSON EXISTS
    "post_customermgmtservice_personexistsbypersonid": "check_person_exists_by_person_id",
    "post_customermgmtservice_personexistsbymobilenumber": "check_person_exists_by_mobile",
    "post_customermgmtservice_personexistsbycifnumber": "check_person_exists_by_cif",
    "post_customermgmtservice_personexistsbycustomfield": "check_person_exists_by_custom",

    # PERSON INFO (LOW LEVEL APIs)
    "post_personinfo_personid": "get_person_info_by_person_id",
    "post_personid_personalinfo": "get_personal_info_by_person_id",
    "post_personid_contactinfo": "get_contact_info_by_person_id",
    "post_personid_metainfo": "get_meta_info_by_person_id",
    "post_personinfo_personalinfo": "get_personal_info_by_mobile",
    "post_personinfo_contactinfo": "get_contact_info_by_mobile",
    "post_personinfo_metainfo": "get_meta_info_by_mobile",
    "post_customermgmt_personinfo": "get_person_full_info",

    # WALLET
    "post_wallet_walletbalance": "get_wallet_balance",
    "post_wallettransfer_walletbalancebyenddate": "get_wallet_balance_by_date",
    "post_wallet_isexist": "check_cbdc_wallet_exists",
    "post_regularwallet_exists": "check_regular_wallet_exists",
    "post_walletmgmtservice_getwalletdetailsbypersonid": "get_wallet_by_personId",
    "post_walletmgmtservice_getwalletdetailsbymobilenumber": "get_wallet_by_mobile",
    "post_walletmgmtservice_getwalletdetailsbycifnumber": "get_wallet_by_cif",
    "post_walletmgmtservice_walletdetailsbymobilenumber": "get_wallet_details_by_mobile",
    "post_walletmgmtservice_walletdetailsbycifnumber": "get_wallet_details_by_cif",
    "post_walletmgmt_walletinfo": "get_wallet_info_by_mobile",
    "post_walletinfo_personid": "get_wallet_info_by_personid",
    "post_walletmgmtservice_getwalletidsbyprogrammanageridandtagid": "list_wallet_ids_by_tag",
    "post_walletmgmtservice_getwalletcountbyprogrammanagerid": "count_wallets",
    "post_walletmgmtservice_getwalletcountbyprogrammanageridandtagid": "count_wallets_by_tag",
    "post_walletmgmtservice_tags": "list_wallet_tags",
    "post_walletmgmtservice_gettagsbyprogrammanageridandgroupid": "list_tags_by_group",

    # PAYMENTS
    "post_wallettransfer_payment": "get_payment_by_txn",
    "post_wallettransfer_payments": "list_payments",
    "post_wallettransfer_paymentsbypersonid": "get_payments_by_person",
    "post_wallettransfer_paymentsbymobilenumber": "get_payments_by_mobile",
    "post_wallettransfer_paymentsbycustomfield": "get_payments_by_custom",

    # PAYMENT STATUS
    "post_wallettransferservice_paymentstatusbytransactionid": "get_payment_status",
    "post_wallettransferservice_paymentstatusbyprogrammanageridandcli": "get_payment_by_client",

    # PAYMENT EXISTS
    "post_wallettransfer_paymentexistsbypersonid": "check_payment_exists_by_person_id",
    "post_wallettransfer_paymentexistsbymobilenumber": "check_payment_exists_by_mobile",
    "post_wallettransfer_paymentexistsbycustomfield": "check_payment_exists_by_custom",

    # RECENT PAYMENTS
    "post_wallettransfer_recentpayments": "get_recent_payments",
    "post_wallettransfer_recentpaymentsbywalletid": "get_recent_by_wallet",
    "post_wallettransfer_recentpaymentsbypersonid": "get_recent_by_person",
    "post_wallettransfer_recentpaymentbymobileno": "get_recent_by_mobile",
    "post_wallettransfer_recentpaymentbywalletid": "get_recent_wallet",
    "post_wallettransfer_recentpaymentbycustomfields": "get_recent_by_custom",
    "post_wallettransfer_recentpaymentsbypersonidwithpagination": "get_recent_person_paginated",

    # UPDATED TRANSFER
    "post_walletupdatedtransfer_recentpaymentsbypersonid": "get_updated_person",
    "post_walletupdatedtransfer_recentpaymentbymobileno": "get_updated_mobile",
    "post_walletupdatedtransfer_recentpaymentbywalletid": "get_updated_wallet",
    "post_walletupdatedtransfer_recentpaymentbycustomfields": "get_updated_custom",
    "post_walletupdatedtransfer_pendingauthorizationpaymentsbypersoni": "get_pending_auth_person",
    "post_walletupdatedtransfer_authorizedpaymentsbypersonid": "get_authorized_person",

    # AUTHORIZATION
    "post_authorization_v1": "get_pending_authorizations",
    "post_authorized_v1": "get_authorized_transfers",
    "post_transfer_pendingauthorization": "get_pending_transfers",
    "post_transfer_authorized": "get_authorized_transfers_simple",

    # TRANSFER TYPES VALIDATION
    "post_transfertype_exists": "check_transfer_type_exists",

    # TRANSFER DATA
    "post_walletinforetrieval_wallettransfers": "get_wallet_transfers",
    "post_wallettransfers_mobilenumber": "get_transfers_by_mobile",
    "post_wallettransfer_getpaymentdonebywalletidandtransfertypeid": "get_payment_by_wallet_type",

    # METRICS
    "post_metrics_countofpaymentsbyprogrammanagerid": "count_payments_by_program_manager",
    "post_metrics_countoftotalpaymentsbyprogrammanagerid": "count_total_payments",
    "post_metrics_countoftotalpaymentsbytimegroup": "count_by_time",
    "post_metrics_countofpaymentsbyprogrammanageridandtransfertypeid": "count_by_program_manager_and_type",
    "post_metrics_countofpaymentsbytimegroupandtransfertypeid": "count_by_time_and_type",

    # SUM
    "post_wallettransfer_sumoftotalamountforalltransfertypesbyprogram": "sum_all_transfers",
    "post_wallettransfer_sumoftotalamountbytransfertypeidandprogramma": "sum_by_type",

    # LOCATIONS
    "post_wallettransfer_paymentlocationsbyprogrammanagerid": "get_payment_locations",
    "post_wallettransfer_paymentlocationsbyprogrammanageridandtransfe": "get_payment_locations_type",

    # PENDING BALANCE
    "post_wallettransferservice_pendingbalance": "get_pending_balance",

    # CUSTOM FIELDS
    "post_customermgmtservice_customfields": "list_customer_custom_fields",
    "post_wallettransferservice_customfields": "list_transfer_custom_fields",

    # PROGRAM MANAGER EVENTS
    "post_programmngrmgmtservice_event": "get_program_event",

    # EVENTS (DEDUPED PROPERLY)
    "post_walletcomplianceservice_event": "get_compliance_event",
    "post_walletmgmtservice_event": "get_wallet_event",
    "post_wallettransferservice_event": "get_transfer_event",
    "post_cbdcwallettransfer_findeventbytransactionid": "get_cbdc_event",
    "post_payment_event": "get_payment_event",
    "post_exception_event": "get_exception_event",
    "post_iamservice_event": "get_iam_event",
    "post_customermgmtservice_event": "get_customer_event",

}

TOOL_DESCRIPTIONS = {
    # PROGRAM / CONFIG
    "list_program_managers": "List all available program managers.",
    "list_transfer_types": "List all transfer types for a given program manager. Requires programManagerId.",
    "list_groups": "List all groups under a given program manager. Requires programManagerId.",
    "list_system_accounts": "List all system accounts under a given program manager. Requires programManagerId.",

    # PERSON
    "get_person_by_person_id": "Get person/customer details using programManagerId and personId.",
    "get_person_by_mobile": "Get person/customer details using programManagerId and mobileNumber.",
    "get_person_by_cif": "Get person/customer details using programManagerId and cifNumber.",
    "get_person_by_wallet": "Get person/customer details linked to a walletId. Use this when the user has walletId and wants person/customer details.",
    "get_person_by_custom": "Get person/customer details using programManagerId, customFieldId, and customFieldValue.",
    "get_person_by_broker": "List person/customer details using programManagerId and brokerId.",
    "get_persons_by_group": "List persons/customers under a group. Requires programManagerId, groupId, pageNumber, and pageSize.",
    "list_person_ids": "List person IDs for a program manager with pagination. Requires programManagerId, pageNumber, and pageSize.",
    "count_registered_persons": "Get total registered person/customer count for a program manager. Requires programManagerId.",

    # PERSON EXISTS
    "check_person_exists_by_person_id": "Check whether a person/customer exists using programManagerId and personId.",
    "check_person_exists_by_mobile": "Check whether a person/customer exists using programManagerId and mobileNumber.",
    "check_person_exists_by_cif": "Check whether a person/customer exists using programManagerId and cifNumber.",
    "check_person_exists_by_custom": "Check whether a person/customer exists using programManagerId, customFieldId, and customFieldValue.",

    # PERSON INFO LOW LEVEL
    "get_person_info_by_person_id": "Get detailed person profile information using personId.",
    "get_personal_info_by_person_id": "Get personal information using personId.",
    "get_contact_info_by_person_id": "Get contact information using personId.",
    "get_meta_info_by_person_id": "Get metadata information using personId.",
    "get_personal_info_by_mobile": "Get personal information using mobileNumber.",
    "get_contact_info_by_mobile": "Get contact information using mobileNumber.",
    "get_meta_info_by_mobile": "Get metadata information using mobileNumber.",
    "get_person_full_info": "Get complete person/customer profile information.",

    # WALLET
    "get_wallet_balance": (
        "Get wallet balance only when walletId, programManagerId, and tagId are known."
    ),
    "get_wallet_balance_by_date": (
        "Get wallet balance as of a specific endDate. Requires walletId, programManagerId, tagId, and endDate. "
        "Use only when walletId and tagId are known."
    ),
    "check_cbdc_wallet_exists": "Check whether a CBDC wallet exists using programMngrId, walletId, and tagId.",
    "check_regular_wallet_exists": "Check whether a regular wallet exists using programMngrId, walletId, and tagId.",
    "get_wallet_by_personId": (
        "Use this FIRST when the user asks for wallet details or wallet balance using personId. "
        "Requires programManagerId and personId. This can return walletId/tagId needed for balance."
    ),
    "get_wallet_by_mobile": (
        "Use this FIRST when the user asks for wallet details or wallet balance using mobileNumber. "
        "Requires programManagerId and mobileNumber. This can return walletId/tagId needed for balance."
    ),
    "get_wallet_by_cif": (
        "Use this FIRST when the user asks for wallet details or wallet balance using cifNumber. "
        "Requires programManagerId and cifNumber. This can return walletId/tagId needed for balance."
    ),
    "get_wallet_details_by_mobile": "Get CBDC wallet details using programManagerId and mobileNumber.",
    "get_wallet_details_by_cif": "Get CBDC wallet details using programManagerId and cifNumber.",
    "get_wallet_info_by_mobile": "Get wallet information using mobileNumber.",
    "get_wallet_info_by_personid": "Get wallet information using personId.",
    "list_wallet_ids_by_tag": "List wallet IDs using programManagerId and tagId.",
    "count_wallets": "Get wallet count for a program manager. Requires programManagerId.",
    "count_wallets_by_tag": "Get wallet count by programManagerId and tagId.",
    "list_wallet_tags": "List wallet tags for a program manager. Requires programManagerId.",
    "list_tags_by_group": "List wallet tags by programManagerId and groupId.",

    # PAYMENTS
    "get_payment_by_txn": "Get payment/transaction details using programManagerId and transactionId.",
    "list_payments": "List payments with pagination. Use for broad payment history when programManagerId and date range are available.",
    "get_payments_by_person": "Get payment/transaction history using programManagerId, personId, startDate, and endDate.",
    "get_payments_by_mobile": "Get payment/transaction history using programManagerId, mobileNo, startDate, and endDate.",
    "get_payments_by_custom": "Get payment/transaction history using programManagerId, customFieldId, customFieldValue, startDate, and endDate.",

    # PAYMENT STATUS
    "get_payment_status": "Get payment status using programManagerId and transactionId.",
    "get_payment_by_client": "Get payment status/details using programManagerId and clientRequestId.",

    # PAYMENT EXISTS
    "check_payment_exists_by_person_id": "Check whether a payment exists using programManagerId, personId, and transferTypeId.",
    "check_payment_exists_by_mobile": "Check whether a payment exists using programManagerId, mobileNo, and transferTypeId.",
    "check_payment_exists_by_custom": "Check whether a payment exists using programManagerId, transferTypeId, customFieldId, and customFieldValue.",

    # RECENT PAYMENTS
    "get_recent_payments": "Get recent payments/transactions using filters such as programManagerId, transferTypeId, transferStatus, startDate, endDate, and limit.",
    "get_recent_by_wallet": "Get recent payments/transactions by walletId. Requires programManagerId, walletId, tagId, transferTypeId, transferStatus, startDate, endDate, and limit.",
    "get_recent_by_person": "Get recent payments/transactions by personId. Requires programManagerId, personId, transferTypeId, transferStatus, startDate, endDate, and limit.",
    "get_recent_by_mobile": "Get recent payments/transactions by mobileNo. Requires programManagerId, mobileNo, transferTypeId, transferStatus, startDate, endDate, and limit.",
    "get_recent_wallet": "Get recent wallet payments using walletId and related filters.",
    "get_recent_by_custom": "Get recent payments by customFieldId/customFieldValue and related filters.",
    "get_recent_person_paginated": "Get paginated recent payments for personId. Use when user asks for transaction history with pagination.",

    # UPDATED TRANSFER
    "get_updated_person": "Get updated-transfer recent payments by personId.",
    "get_updated_mobile": "Get updated-transfer recent payments by mobileNo.",
    "get_updated_wallet": "Get updated-transfer recent payments by walletId.",
    "get_updated_custom": "Get updated-transfer recent payments by custom field.",
    "get_pending_auth_person": "Get pending authorization payments for a personId.",
    "get_authorized_person": "Get authorized payments for a personId.",

    # AUTHORIZATION
    "get_pending_authorizations": "Get paginated pending authorization transfers for a program manager.",
    "get_authorized_transfers": "Get paginated authorized transfers for a program manager.",
    "get_pending_transfers": "Get pending authorization transfers for a program manager.",
    "get_authorized_transfers_simple": "Get authorized transfers for a program manager.",

    # TRANSFER TYPE VALIDATION
    "check_transfer_type_exists": "Check whether a transfer type exists.",

    # TRANSFER DATA
    "get_wallet_transfers": "Get wallet transfer details.",
    "get_transfers_by_mobile": "Get transfer details using mobileNumber.",
    "get_payment_by_wallet_type": "Get payments using programManagerId, walletId, tagId, groupId, and transferTypeId.",

    # METRICS
    "count_payments_by_program_manager": "Count payments by programManagerId and date range.",
    "count_total_payments": "Count total payments by programManagerId and date range.",
    "count_by_time": "Count total payments grouped by DAY, WEEK, or MONTH. Requires programManagerId, startDate, endDate, and transactionTimeSegment.",
    "count_by_program_manager_and_type": "Count payments by programManagerId, transferTypeId, and date range.",
    "count_by_time_and_type": "Count payments grouped by time segment and transferTypeId.",

    # SUM
    "sum_all_transfers": "Get total amount across all transfer types for a program manager and date range.",
    "sum_by_type": "Get total amount for a specific transferTypeId, programManagerId, and date range.",

    # LOCATIONS
    "get_payment_locations": "Get payment locations for a program manager and date range.",
    "get_payment_locations_type": "Get payment locations for a program manager, transferTypeId, and date range.",

    # PENDING BALANCE
    "get_pending_balance": "Get pending transaction balance using programManagerId, WalletId, and TagId.",

    # CUSTOM FIELDS
    "list_customer_custom_fields": "List customer custom fields for a program manager.",
    "list_transfer_custom_fields": "List transfer/payment custom fields for a program manager.",

    # PROGRAM MANAGER EVENTS
    "get_program_event": "Get program manager event using transactionId.",

    # EVENTS
    "get_compliance_event": "Get compliance event using transactionId.",
    "get_wallet_event": "Get wallet event using transactionId.",
    "get_transfer_event": "Get transfer event using transactionId.",
    "get_cbdc_event": "Get CBDC transfer event using transactionId.",
    "get_payment_event": "Get payment event using transactionId.",
    "get_exception_event": "Get exception event using transactionId.",
    "get_iam_event": "Get IAM event using transactionId.",
    "get_customer_event": "Get customer event using transactionId.",
}