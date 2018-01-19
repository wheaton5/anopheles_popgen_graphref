#!/software/python-2.7.6/bin/python
import subprocess

def split(args):
    chunks = []
    for sample, bam in args.bams.iteritems():
        chunks.append({'bam':bam, 'sample_name':sample, '__mem_gb':8,'__threads':1})
    return {'chunks':chunks,'join':{'mem_bg':2}}


def main(args, outs):
    outs.coerce_strings()
    args.coerce_strings()
    subprocess.check_call(['samtools','sort','-n',args.bam,args.bam.strip(".bam")+"qsort"])
    subprocess.check_call(['bamToFastq','-i',args.bam.strip(".bam")+"qsort.bam",'-fq',args.bam.strip(".bam")+".fq"])
    subprocess.check_call(['gzip', args.bam.strip(".bam")+".fq"])
    outs.fastq = args.bam.strip(".bam")+".fq.gz"
    outs.sample_name = args.sample_name

def join(args, outs, chunk_defs, chunk_outs):
    outs.fastqs = {}
    for chunk_out in chunk_outs:
        outs.fastqs[chunk_outs.sample_name] = chunk_out.fastq

