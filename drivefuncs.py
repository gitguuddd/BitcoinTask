import sys
import traceback
import logging
import globals
import binascii
import hashlib
from bitcoin.rpc import RawProxy


def input_txid():
    txid = input()
    if not len(txid) == 64:
        while True:
            print('Ivestas transakcijos id yra per trumpas/per ilgas (ne 64 simboliu) - bandykite dar karta')
            txid = input()
            if len(txid) == 64:
                break
    return txid


def to_little_endian(hexstring):
    ba = bytearray.fromhex(hexstring)
    ba.reverse()
    s = ''.join(format(x, '02x') for x in ba)
    return s


def get_blockhash():
    p = RawProxy()
    print('Iveskite tikrinamo bloko numeri')
    height = input()
    try:
        blockhash = p.getblockhash(int(height))
        return blockhash
    except Exception as e:
        logging.error(traceback.format_exc())
        globals.control = 0
        return


def get_utxo(index, txid):
    p = RawProxy()
    raw_tx = p.getrawtransaction(txid)
    decoded_tx = p.decoderawtransaction(raw_tx)
    outputs = decoded_tx['vout']
    utxo = outputs[index]
    return utxo['value']


def end_execution():
    sys.exit()


def find_transaction_fee():
    p = RawProxy()
    print('Iveskite pasirinktos transakcijos id')
    txid = input_txid()
    txinval = 0
    txoutval = 0
    try:
        raw_tx = p.getrawtransaction(txid)
    except Exception as e:
        logging.error(traceback.format_exc())
        globals.control = 0
        return
    decoded_tx = p.decoderawtransaction(raw_tx)
    vins = decoded_tx['vin']
    vouts = decoded_tx['vout']
    for input in vins:
        txinval = txinval + get_utxo(input['vout'], input['txid'])
    for output in vouts:
        txoutval = txoutval + output['value']
    globals.control = 0
    print('Transakcijos kaina:')
    print(f'{txinval - txoutval} BTC')
    return


def check_block():
    p = RawProxy()
    var = get_blockhash()
    if var is None:
        return
    header = p.getblockheader(var)
    header_hex = (to_little_endian(header['versionHex']) + to_little_endian(header['previousblockhash'])
                  + to_little_endian(header['merkleroot']) + to_little_endian(format(int(header['time']), 'x'))
                  + to_little_endian(header['bits']) + to_little_endian(format(int(header['nonce']), 'x')))

    header_bin = binascii.unhexlify(header_hex)
    block_hask = hashlib.sha256(hashlib.sha256(header_bin).digest()).hexdigest()
    block_hask_le = to_little_endian(block_hask)
    if var == block_hask_le:
        print('Bloko hashas yra teisingas')
    else:
        print('Bloko hashas yra neteisingas')
    globals.control = 0
