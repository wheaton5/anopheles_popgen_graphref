#!/software/python-2.7.6/bin/python
import subprocess

def split(args):
    chunks = []
    for fastq in args.fastqs:
        chunks.append({'fastq':fastq, '__mem_gb':20,'__threads':16})
    return {'chunks':chunks,'join':{'mem_bg':2}}


def main(args, outs):
    outs.coerce_strings()
    with open(outs.assembly.strip(".mag.gz")+".mak",'w') as assembly:
        subprocess.check_call(['/nfs/users/nfs_h/hh5/bin/fermi.kit/fermi2.pl','unitig','-s300m', '-t16','-l100','-p','assembly', args.fastq],stdout=assembly)
    subprocess.check_call(['make','-f',outs.assembly.strip('.mag.gz')+".mak"])
    ps = subprocess.Popen(['/nfs/users/nfs_h/hh5/bin/fermi.kit/run-calling','-t16','/lustre/scratch118/malaria/team222/hh5/ref/Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.fa',outs.assembly], stdout=subprocess.PIPE) 
    subprocess.check_call(['sh'], stdin=ps.stdout)
    ps.wait()
    
def join(args, outs, chunk_defs, chunk_outs):
    outs.assembly = []
    outs.vcf = []
    for chunk_out in chunk_outs:
        outs.assembly.append(chunk_out.assembly)
        outs.vcf.append(chunk_out.vcf)

