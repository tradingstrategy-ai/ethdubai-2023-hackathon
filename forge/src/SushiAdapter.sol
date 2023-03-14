// SPDX-License-Identifier: GPL-3.0

pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

import "@enzyme/release/extensions/integration-manager/integrations/utils/AdapterBase.sol";

/**
 * SushiSwap adapter for Enzyme vaults.
 *
 * - Based on "GenericAdapter" example of Enzyme Protocol
 *
 * - Uses server-side prepared signatures to trade on Sushi
 *
 */
contract SushiAdapter is AdapterBase {

    // Tell enzyme what is our selector when we call this adapter
    bytes4 public constant EXECUTE_CALLS_SELECTOR = bytes4(
        keccak256("executeCalls(address,bytes,bytes)")
    );

    constructor(address _integrationManager) public AdapterBase(_integrationManager) {}

    // EXTERNAL FUNCTIONS

    /// @notice Executes a sequence of calls
    /// @param _vaultProxy The VaultProxy of the calling fund
    /// @param _actionData Data specific to this action
    function executeCalls(
        address _vaultProxy,
        bytes calldata _actionData,
        bytes calldata
    )
        external
        onlyIntegrationManager
        postActionIncomingAssetsTransferHandler(_vaultProxy, _actionData)
        postActionSpendAssetsTransferHandler(_vaultProxy, _actionData)
    {
        (, , , , bytes memory externalCallsData) = __decodeCallArgs(_actionData);

        (address[] memory contracts, bytes[] memory callsData) = __decodeExternalCallsData(
            externalCallsData
        );

        for (uint256 i; i < contracts.length; i++) {
            address contractAddress = contracts[i];
            bytes memory callData = callsData[i];
            (bool success, bytes memory returnData) = contractAddress.call(callData);
            require(success, string(returnData));
        }
    }

    /// @notice Parses the expected assets in a particular action
    /// @param _selector The function selector for the callOnIntegration
    /// @param _actionData Data specific to this action
    /// @return spendAssetsHandleType_ A type that dictates how to handle granting
    /// the adapter access to spend assets (hardcoded to `Transfer`)
    /// @return spendAssets_ The assets to spend in the call
    /// @return spendAssetAmounts_ The max asset amounts to spend in the call
    /// @return incomingAssets_ The assets to receive in the call
    /// @return minIncomingAssetAmounts_ The min asset amounts to receive in the call
    function parseAssetsForAction(
        address,
        bytes4 _selector,
        bytes calldata _actionData
    )
        external
        view
        override
        returns (
            IIntegrationManager.SpendAssetsHandleType spendAssetsHandleType_,
            address[] memory spendAssets_,
            uint256[] memory spendAssetAmounts_,
            address[] memory incomingAssets_,
            uint256[] memory minIncomingAssetAmounts_
        )
    {
        require(_selector == EXECUTE_CALLS_SELECTOR, "parseAssetsForAction: _selector invalid");

        (
            incomingAssets_,
            minIncomingAssetAmounts_,
            spendAssets_,
            spendAssetAmounts_,

        ) = __decodeCallArgs(_actionData);

        return (
            IIntegrationManager.SpendAssetsHandleType.Transfer,
            spendAssets_,
            spendAssetAmounts_,
            incomingAssets_,
            minIncomingAssetAmounts_
        );
    }

    /// @dev Helper to decode the encoded callOnIntegration call arguments
    function __decodeCallArgs(bytes calldata _actionData)
        private
        pure
        returns (
            address[] memory incomingAssets_,
            uint256[] memory minIncomingAssetsAmounts_,
            address[] memory spendAssets_,
            uint256[] memory spendAssetAmounts_,
            bytes memory externalCallsData_
        )
    {
        return abi.decode(_actionData, (address[], uint256[], address[], uint256[], bytes));
    }

    /// @dev Helper to decode the stack of external contract calls
    function __decodeExternalCallsData(bytes memory _externalCallsData)
        private
        pure
        returns (address[] memory contracts_, bytes[] memory callsData_)
    {
        (contracts_, callsData_) = abi.decode(_externalCallsData, (address[], bytes[]));
        require(contracts_.length == callsData_.length, "Unequal external calls arrays lengths");
        return (contracts_, callsData_);
    }
}
