#!/software/python-2.7.6/bin/python
import subprocess
import pyfasta

def split(args):
    chunks = []
    for sample, (gams, gam_indexes, vgs) in args.gams.iteritems():
        for (gam, gam_index, vg) in zip(gams, gam_indexes, vgs):
            chunks.append({'gam':gam,'gam_index':gam_index,'vg':vg,'sample_name':
                sample_name,'__mem_gb':8,'__threads':8}) 
        
    return {'chunks':chunks,'join':{'__mem_gb':8}}


def main(args, outs):
    outs.coerce_strings()
    args.coerce_strings()
    
    with open(outs.vcf.strip('.gz')) as tmp:
        subprocess.check_call(['vg','genotype',args.vg, args.gam_index],stdout=tmp)
    subprocess.check_call(['bgzip',outs.vcf.strip('.gz')])
    subprocess.check_call(['tabix','-p','vcf',outs.vcf])
    outs.sample_name = args.sample_name
    
def join(args, outs, chunk_defs, chunk_outs):
    outs.vcfs = {}
    vcfs = {}
    for chunk_out in chunk_outs:
        sample_vcfs = vcfs.setdefault('sample_index',[])
        sample_vcfs.append(chunk_out.vcf)
    for sample, vcf_list in vcfs.iteritems():
        vcf_list = sorted(vcf_list)
        command = ['bcftools','concat']
        command.extend(vcf_list)
        with open(outs.vcf[0:-7]+sample+".vcf",'w') as vcfout:
            subprocess.check_call(command, stdout=vcfout)
        subprocess.check_call(['bgzip', outs.vcf[0:-7]+sample+".vcf"])
        subprocess.check_call(['tabix','-p','vcf',outs.vcf[0:-7]+sample+".vcf.gz"])
        outs.vcfs[sample] = outs.vcf[0:-7]+sample+".vcf.gz"
