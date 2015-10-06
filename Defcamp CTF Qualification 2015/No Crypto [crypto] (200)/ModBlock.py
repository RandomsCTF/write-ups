def mod_block(plaintext, mod, prev_block):
    diff = [ord(a) ^ ord(b) for a, b in zip(plaintext[:16], mod[:16])]
    return ''.join(["%0.2x" % (int(prev_block[i*2:i*2+2], 16) ^ diff[i]) for i in range(16)])

if __name__ == "__main__":
    print mod_block(
        'Pass: sup3r31337',
        'Pass: notAs3cre7',
        '19a9d10c3b155b55982a54439cb05dce',
    )
