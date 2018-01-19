#!/software/python-2.7.6/bin/python
import subprocess
import pyfasta

def split(args):
    chunks = []
    fasta = pyfasta.Fasta("/lustre/scratch118/malaria/team222/hh5/ref/Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.fa")
    
    for key in fasta.keys():
        start = 1
        step = 20000000
        if args.locus:
            chrom = args.locus.split(":")[0]
            start = args.locus.split(":")[1].split("-")[0]
            end = args.locus.split("-")[1]
            if key == chrom:
                chunks.append({'vcfs':args.vcfs, 'chrom':key+":"+start+"-"+end,'__mem_gb':8,'__threads':1})
        else:
            chunks.append({'vcfs':args.vcfs,'chrom':key,'__mem_gb':8,'__threads':1})
        
    return {'chunks':chunks,'join':{'__mem_gb':8}}


def main(args, outs):
    outs.coerce_strings()
    args.coerce_strings()
    with open(outs.reference,'w') as outfile:
        command = ['vg','construct','-t','1','-R',args.chrom,'-r',
            '/lustre/scratch118/malaria/team222/hh5/ref/Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.fa','-v']
        command.extend(args.vcfs)
        print command
        subprocess.check_call(command,stdout = outfile)
    
def join(args, outs, chunk_defs, chunk_outs):
    outs.reference = []
    for chunk_out in chunk_outs:
        outs.reference.append(chunk_out.reference)
    command = ['vg','ids','-j']
    command.extend(outs.reference)
    subprocess.check_call(command)
    command = ['vg','index','-x',outs.xg]
    command.extend(outs.reference)
    subprocess.check_call(command)
