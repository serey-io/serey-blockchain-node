# Introducing Serey (beta)

Serey is a Delegated Proof of Stake blockchain that uses a Democratic voting system to organize content by visibility and relevance. The blockchain is a central connecting point to the Serey ecosystem of dApps and websites. 

    • Currency symbol SRY
    • 1,5% Annual inflation 
    • 33,33% of the inflation to rewarding the content and the curation
    • 33,33% of the inflation to stakeholders in Serey Power
    • 33,33% of inflation to witnesses/block producers

Serey ecosystem of dApps:
    1. Serey.io (web and mobile)
    2. Serey Market place (web)
    3. Serey Poker (web)
    4. Serey Football (web)
    5. Serey DEX (web)
    6. Serey Lottery (under construction)
    7. More..

# Public Announcement & Discussion

Serey was announced on Medium.com by an article written by one of the founders Chhay Lin Lim in 2018: https://medium.com/@chhaylin

# No Support & No Warranty

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.

# Whitepaper

You can read the Serey Whitepaper at: https://serey.io/static/media/serey-white-paper-2020.ddd99c95.pdf


# Building

We strongly recommend using one of our pre-built Docker images or using Docker to build Serey.


## Dockerized p2p Node

To run a p2p node (ca. 2GB of memory is required at the moment):

   sudo docker run --rm -it -p 8090:8090 -p 2001:2001 -v /opt/witness_node_data_dir:/opt/witness_node_data_dir sereyio/sereyd:latest /opt/steemd -d /opt/witness_node_data_dir

## Dockerized Full Node

To run a node with *all* the data (e.g. for supporting a content website)
that uses ca. 14GB of memory and growing:

 sudo docker run --rm -it -p 8090:8090 -p 2001:2001 -v /opt/witness_node_data_dir:/opt/witness_node_data_dir sereyio/sereyd:latest /opt/steemd -d /opt/witness_node_data_dir

# Environment variables

There are quite a few environment variables that can be set to run steemd in different ways:

* `USE_WAY_TOO_MUCH_RAM` - if set to true, steemd starts a 'full node'
* `USE_FULL_WEB_NODE` - if set to true, a default config file will be used that enables a full set of API's and associated plugins.
* `USE_NGINX_FRONTEND` - if set to true, this will enable an NGINX reverse proxy in front of steemd that proxies websocket requests to steemd. This will also enable a custom healtcheck at the path '/health' that lists how many seconds away from current blockchain time your node is. It will return a '200' if it's less than 60 seconds away from synced.
* `USE_MULTICORE_READONLY` - if set to true, this will enable steemd in multiple reader mode to take advantage of multiple cores (if available). Read requests are handled by the read-only nodes, and write requests are forwarded back to the single 'writer' node automatically. NGINX load balances all requests to the reader nodes, 4 per available core. This setting is still considered experimental and may have trouble with some API calls until further development is completed.
* `HOME` - set this to the path where you want steemd to store it's data files (block log, shared memory, config file, etc). By default `/var/lib/steemd` is used and exists inside the docker container. If you want to use a different mountpoint (like a ramdisk, or a different drive) then you may want to set this variable to map the volume to your docker container.


# System Requirements

For a full web node, you need at least 110GB of disk space available. Steemd uses a memory mapped file which currently holds 56GB of data and by default is set to use up to 80GB. The block log of the blockchain itself is a little over 27GB. It's highly recommended to run steemd on a fast disk such as an SSD or by placing the shared memory files in a ramdisk and using the `--shared-file-dir=/path` command line option to specify where. At least 16GB of memory is required for a full web node. Seed nodes (p2p mode) can run with as little as 4GB of memory with a 16 GB state file. Any CPU with decent single core performance should be sufficient. Steemd is constantly growing. As of August 2017, these numbers were accurate, but you may find you need more disk space to run a full node. We are also constantly working on optimizing Steem's use of disk space.

On Linux use the following Virtual Memory configuration for the initial sync and subsequent replays. It is not needed for normal operation.

```
echo    75 | sudo tee /proc/sys/vm/dirty_background_ratio
echo  1000 | sudo tee /proc/sys/vm/dirty_expire_centisec
echo    80 | sudo tee /proc/sys/vm/dirty_ratio
echo 30000 | sudo tee /proc/sys/vm/dirty_writeback_centisec
```
