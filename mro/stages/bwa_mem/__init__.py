#!/software/python-2.7.6/bin/python
import subprocess

def split(args):
    chunks = []
    for sample, fastq in args.fastqs.iteritems():
        chunks.append({'fastq':fastq, 'sample_name':sample,'__mem_gb':8,'__threads':8})
    return {'chunks':chunks,'join':{'mem_bg':2}}


def main(args, outs):
    outs.coerce_strings()
    args.coerce_strings()
    #subprocess.check_call(['gzip',args.fastq])
    with open(outs.sam,'w') as samfile:
        subprocess.check_call(['bwa','mem','-M','-t','8','-p','/lustre/scratch118/malaria/team222/hh5/ref/Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.fa',args.fastq], stdout = samfile)
    outs.sample_name = sample_name

def join(args, outs, chunk_defs, chunk_outs):
    outs.sams = {}
    for chunk_out in chunk_outs:
        outs.sams[chunk_out.sample_name] = chunk_out.sam

