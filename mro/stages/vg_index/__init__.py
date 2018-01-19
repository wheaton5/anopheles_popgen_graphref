#!/software/python-2.7.6/bin/python
import subprocess
import pyfasta

def split(args):
    chunks = [{}]
    return {'chunks':chunks,'join':{'__threads':16,'__mem_gb':30}}


def main(args, outs):
    pass
    
def join(args, outs, chunk_defs, chunk_outs):
    for chrom in args.reference:
        with open(chrom.strip(".vg")+".prune.vg",'w') as prune:
            subprocess.check_call(['vg','mod','-t','16','-e','4',chrom],stdout = prune)
        with open(chrom.strip(".vg")+"ref.vg",'w') as refout:
            subprocess.check_call(['vg','mod','-t','16','-N',chrom],stdout=refout)
        with open(chrom.strip(".vg")+".smooth.vg",'w') as smooth:
            with open(chrom.strip(".vg")+"merge.err",'w') as err:
                ps = subprocess.Popen(["cat", chrom.strip(".vg")+"ref.vg"],stdout=subprocess.PIPE)
                subprocess.check_call(['vg','view','-v','-D','-'],stdin=ps.stdout,stderr=err, stdout = smooth)
        with open(chrom.strip(".vg")+".graph",'w') as graph:
            subprocess.check_call(['vg','kmers','-gBk','16','-H','1000000000','-T','1000000001', chrom.strip(".vg")+".smooth.vg"],stdout =graph)
    command = ['vg','index','-g', outs.gcsa,'-Z','3000','-X','3','-t','32']
    for chrom in args.reference:
        command.extend(['-i',chrom.strip(".vg")+".graph"])
    subprocess.check_call(command)
