#!/software/python-2.7.6/bin/python
import subprocess

def split(args):
    chunks = []
    for bam_fn in args.bam_fns:
        chunks.append({'bam_fn':bam_fn})
    return {'chunks':chunks,'join':{'mem_bg':2}}


def main(args, outs):
    outs.coerce_strings()
    args.coerce_strings()
    bam_fn = args.bam_fn.replace("-","_")
    bam_out = '/lustre/scratch118/malaria/team222/hh5/bams/children/'+bam_fn+".bam"
    index_out = '/lustre/scratch118/malaria/team222/hh5/bams/children/'+bam_fn+".bam.bai"
    fq_out = '/lustre/scratch118/malaria/team222/hh5/bams/children/'+bam_fn+".fq.gz"
    subprocess.check_call(['scp','haynes@echo.well.ox.ac.uk://kwiat/2/mirror/vector/bam/bwa_gatk/'+bam_fn+'.bam*', '/lustre/scratch118/malaria/team222/hh5/bams/children/.'])
    subprocess.check_call(['bamToFastq','-i', bam_out,'-fq',fq_out.strip(".gz")])
    subprocess.check_call(['gzip',fq_out.strip('.gz')])
    outs.fastq = fq_out
    outs.bam = bam_out
    outs.index = index_out
    
def join(args, outs, chunk_defs, chunk_outs):
    outs.coerce_strings()
    outs.bams = []
    outs.indexes = []
    outs.fastqs = []
    for chunk_out in chunk_outs:
        outs.bams.append(chunk_out.bam)
        outs.indexes.append(chunk_out.index)
        outs.fastqs.append(chunk_out.fastq)
