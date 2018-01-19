#!/software/python-2.7.6/bin/python
import subprocess

def split(args):
    chunks = []
    for sample, sam in args.sams.iteritems():
        chunks.append({'sam':sam, 'sample_name':sample_name,'__mem_gb':8,'__threads':1})
    return {'chunks':chunks,'join':{'mem_bg':2}}


def main(args, outs):
    outs.coerce_strings()
    args.coerce_strings()
    with open(outs.bam[0:-4]+"tmp.bam",'w') as bamfile:
        subprocess.check_call(['samtools', 'view','-bT','/lustre/scratch118/malaria/team222/hh5/ref/Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.fa', args.sam],stdout = bamfile)
    subprocess.check_call(['samtools','sort', outs.bam[0:-4]+"tmp.bam", outs.bam[0:-4]+"md"])
    
    subprocess.check_call(['java','-Xmx7G','-jar','/nfs/users/nfs_h/hh5/bin/picard.jar',
        'MarkDuplicates','ASSUME_SORTED=true','METRICS_FILE='+outs.bam[0:-4]+"metrics.txt",
        'INPUT='+outs.bam[0:-4]+"md.bam",'OUTPUT='+outs.bam])
    subprocess.check_call(['samtools','index',outs.bam, outs.bam+".bai"])
    outs.sample_name = args.sample_name
    outs.bam_index = outs.bam+".bai"

def join(args, outs, chunk_defs, chunk_outs):
    outs.bams = {}
    for chunk_out in chunk_outs:
        outs.bams[chunk_out.sample_name] = chunk_out.bam
        outs.bam_indexes[chunk_out.sample_name] = chunk_out.bam_index
