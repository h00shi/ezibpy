#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# ezIBpy: a Pythonic Client for Interactive Brokers API
# https://github.com/ranaroussi/ezibpy
#
# Copyright 2015 Ran Aroussi
#
# Licensed under the GNU Lesser General Public License, v3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ezibpy
import time

# initialize ezIBpy
ibConn = ezibpy.ezIBpy()
ibConn.connect(clientId=100, host="localhost", port=4001)

# create a contract
contract = ibConn.createFuturesContract("ES", exchange="GLOBEX", expiry="201609")

# submit a bracket order (entry=0 = MKT order)
order = ibConn.createBracketOrder(contract, quantity=1, entry=0, target=2200., stop=1900.)

# let order fill
time.sleep(3)

# see the positions
print("Positions")
print(ibConn.positions)

# create a trailing stop that's triggered at 2190
symbol = ibConn.contractString(contract)

ibConn.createTriggerableTrailingStop(symbol, -1,
            triggerPrice  = 2190,
            trailAmount   = 10, # for trail using fixed amount
            # trailPercent  = 10, # for trail using percentage
            parentId      = order['entryOrderId'],
            stopOrderId   = order["stopOrderId"]
        )

# NOTE: the stop trigger/trailing is done by the software,
# so your script needs to keep running for this functionality to work!

while True:
    time.sleep(1)
# disconnect
# ibConn.disconnect()
