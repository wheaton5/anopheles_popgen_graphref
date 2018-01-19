#!/software/python-2.7.6/bin/python
import subprocess
import glob
import gzip
import vcf
import pyfasta

def split(args):
    variant_filenames = glob.glob("/lustre/scratch118/malaria/team222/hh5/vcfs/AR2/ag1000*PASS.vcf.gz")
    fasta = pyfasta.Fasta("/lustre/scratch118/malaria/team222/hh5/ref/Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.fa")
    print variant_filenames
    chromosomes = [x.split("/lustre/scratch118/malaria/team222/hh5/vcfs/AR2/ag1000g.phase1.AR2.")[1].
                    split(".PASS")[0] for x in variant_filenames]
    print chromosomes
    chromosome_lengths = {}
    for chrom in chromosomes:
        chromosome_lengths[chrom] = len(fasta[chrom])
    chunks = []
    for (vcf, chrom) in zip(variant_filenames, chromosomes):
        chr_length = chromosome_lengths[chrom]
        start = 0
        step = 750000
        while start < chr_length:
            locus = str(chrom)+":"+str(start)+"-"+str(start+step)
                
            chunks.append({'vcf':vcf, 'locus': locus, '__mem_gb':4})
            start += step
    return {'chunks':chunks,'join':{'__mem_gb':2}}

def main(args, outs):
    print args.vcf
    args.coerce_strings()
    chrom = args.locus.split(":")[0]
    start = int(args.locus.split(":")[1].split("-")[0])
    end = int(args.locus.split("-")[1])
    out_fn = outs.vcf.strip('.gz')#args.vcf.strip('.vcf.gz')+"_pop_filtered2.vcf" #outs.default.strip('.gz')
    with open(args.vcf,'r') as vcf_file:
        vcf_reader = vcf.Reader(vcf_file, compressed=True)
        with open(out_fn,'w') as output_file:
            vfw = vcf.Writer(output_file, vcf_reader)
            for record in vcf_reader.fetch(chrom, start, end):
                freq = get_var_frequency(record)
                if freq > 0.02:
                    vfw.write_record(record)
    subprocess.check_call(['bgzip',out_fn])
    subprocess.check_call(['tabix', '-p', 'vcf', out_fn+".gz"])
    outs.chrom = chrom
    outs.start = start

def get_var_frequency(record):
    hets = len(record.get_hets())
    homs = len(record.get_hom_alts())
    refs = len(record.get_hom_refs())*2
    return float(hets+homs*2)/float(refs+homs*2+hets*2)
    

def join(args, outs, chunk_defs, chunk_outs):
    
    chrom = []
    for chunk_out in chunk_outs:
        chunk_out.coerce_strings()
        chrom.append((chunk_out.chrom, chunk_out.start, chunk_out.vcf))
    chrom = sorted(chrom)
    vcfs = []
    for (_,_,vcf) in chrom:
        vcfs.append(vcf)
    command = ['bcftools', 'concat']
    command.extend(vcfs)
    with open(outs.vcf.strip(".gz"), 'w') as out:
        subprocess.call(command, stdout = out)
    subprocess.check_call(['bgzip',outs.vcf.strip(".gz")])
    subprocess.check_call(['tabix','-p','vcf',outs.vcf])
    
''' 
    vcfs = []
    for chunk_out in chunks_outs:#key in chrom.keys():
        vcfs.append(chunk_out.vcf)
    
    command = ['bcftools', 'concat']
    command.extend(vcfs)
    #command.append(outs.vcf.strip(".gz"))
    with open(outs.vcf+"tmp", 'w') as tmp:
        subprocess.call(command, stdout=tmp)
    print "concated"
    with open(outs.vcf.strip(".gz"),'w') as out:
        subprocess.call(['bcftools','sort', outs.vcf+"tmp"],stdout=out)
    print "sorted"
    subprocess.call(['gzip',outs.vcf.strip(".gz")])
    print "ziped"
    subprocess.call(['tabix','index',outs.vcf])
    print "indexed"
'''
