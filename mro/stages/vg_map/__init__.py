#!/software/python-2.7.6/bin/python
import subprocess
import pyfasta

def split(args):
    chunks = []
    
    for (sample_name, fastq) in args.fastqs.iteritems():
        chunks.append({'fastq':fastq, 'sample_name':sample_name, '__mem_gb':8,'__threads':16})
        
    return {'chunks':chunks,'join':{'__mem_gb':8}}


def main(args, outs):
    outs.coerce_strings()
    args.coerce_strings()
    with open(outs.gam,'w') as gamfile:
        subprocess.check_call(['vg','map','-if',args.fastq,'-x',args.xg,'-g',args.gcsa,'-t',str(args.__threads),'-S','0','-u','1','-m','1'],stdout = gamfile)
    outs.sample_name = args.sample_name    

def join(args, outs, chunk_defs, chunk_outs):
    outs.gams = {}
    for chunk_out in chunk_outs:
        outs.gams[chunk_out.sample_name] = chunk_out.gam
