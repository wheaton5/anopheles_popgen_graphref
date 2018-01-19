#!/software/python-2.7.6/bin/python
import subprocess
import glob

def split(args):
    chunks = []
    for (sample_name, gam) in args.gams.iteritems():
        chunks.append({'sample_name': sample_name, 'gam': gam, '__mem_gb':8,'__threads':16})
        
    return {'chunks':chunks,'join':{'__mem_gb':8}}


def main(args, outs):
    outs.coerce_strings()
    args.coerce_strings()
    # make gam index
    gam_index = args.gam+".index"
    subprocess.check_call(['vg','index','-d',gam_index,'-N',args.gam])
    subprocess.check_call(['vg','chunk','-c',args.chunk_size,'-p',outs.gam[0:-4],'-s',args.chunk_size,'-o',args.overlap,'-x',args.xg,'-a',gam_index,'-g','-t',args.__threads,'-E',args.gam[0:-4]+".bed"])
    outs.gam_index = sorted(glob.glob(outs.gam[0:-4]+"*.gam.index"))
    outs.sample_name = args.sample_name
    outs.gam = sorted(glob.glob(outs.gam[0:-4]+"*.gam"))
    outs.vg = sorted(glob.glob(outs.gam[0:-4]+"*.vg"))
    
def join(args, outs, chunk_defs, chunk_outs):
    outs.all_gams = {}
    for chunk_out in chunk_outs:
        outs.all_gams[chunk_out.sample_name] = (chunk_out.gam, chunk_out.gam_index, chunk_out.vg)
