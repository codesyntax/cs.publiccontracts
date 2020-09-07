# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from plone import api
from cs.publiccontracts.contract import IContract
from Products.CMFPlone.resources import add_bundle_on_request


class ContractsFolderView(BrowserView):
    def __call__(self):
        add_bundle_on_request(self.request, "cs.publiccontracts")
        return self.index()

    def contracts_dict(self):
        context = aq_inner(self.context)
        states_dict = context.states
        catalog = api.portal.get_tool("portal_catalog")
        states_list = []
        contracts_path = "/".join(context.getPhysicalPath())
        if not states_dict:
            state_dict = {}
            contracts = catalog(
                object_provides=IContract.__identifier__,
                review_state="published",
                sort_on="effective",
                sort_order="reverse",
                path=contracts_path,
            )
            state_dict["contracts"] = contracts
            state_dict["title"] = ""
            state_dict["value"] = ""
            states_list.append(state_dict)
            return states_list

        for state in states_dict:
            state_dict = {}
            state_value = state["value"]
            contracts = catalog(
                object_provides=IContract.__identifier__,
                review_state="published",
                contract_state=state_value,
                sort_on="effective",
                sort_order="reverse",
                path=contracts_path,
            )
            state_dict["title"] = state["name"]
            state_dict["value"] = state["value"]
            state_dict["contracts"] = contracts

            states_list.append(state_dict)
        return states_list
