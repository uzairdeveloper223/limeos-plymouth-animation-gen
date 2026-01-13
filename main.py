#!/usr/bin/env python3
"""LimeOS Plymouth Boot Animation Generator"""
import os,sys,math,subprocess as sp;from pathlib import Path
try:from PIL import Image,ImageDraw,ImageFont;import cairosvg
except:sp.run([sys.executable,"-m","pip","install","pillow","cairosvg"],check=1);from PIL import Image,ImageDraw,ImageFont;import cairosvg

# ============================================================================
# CONFIGURATION - modify if u wanna to but don't question me if it don't work
# ============================================================================

# Resolution and timing
WIDTH = 1920                    # Output width in pixels
HEIGHT = 1080                   # Output height in pixels
FPS = 30                        # Frames per second
TOTAL_FRAMES = 150              # Total animation frames

# Theme colors (light theme: white bg, black elements)
BG_COLOR = (255, 255, 255)      # Background color (RGB)
TEXT_COLOR = (0, 0, 0)          # Text color (RGB)
DOT_COLOR = (0, 0, 0)           # Spinner dots color (RGB)

# Logo sizes during animation
LOGO_BIG = 400                  # Initial large logo size
LOGO_SMALL = 120                # Final small logo size

# Final element positions (after animation settles)
FINAL_LOGO_X = 840              # Logo X position
FINAL_LOGO_Y = 460              # Logo Y position
FINAL_TEXT_X = 900              # Text X position
FINAL_TEXT_Y = 420              # Text Y position
FINAL_DOTS_Y = 800              # Spinner Y position (centered on X)

# ============================================================================
# fah this end here
# ============================================================================

_D=Path(__file__).parent;_S='''<svg xmlns="http://www.w3.org/2000/svg" width="130" height="130" viewBox="0 0 30 30" fill="none"><path fill="{c}" fill-rule="evenodd" d="M14.5.5C22.508.5 29 6.992 29 15s-6.492 14.5-14.5 14.5S0 23.008 0 15 6.492.5 14.5.5Zm0 1.442C7.288 1.942 1.442 7.788 1.442 15S7.288 28.058 14.5 28.058 27.558 22.212 27.558 15 21.712 1.942 14.5 1.942Z" clip-rule="evenodd"/><path fill="{c}" d="M12.347 18.225c.534-.534 1.448-.156 1.448.6v6.444c0 .489-.414.88-.898.81a11.135 11.135 0 0 1-5.05-2.078c-.395-.292-.413-.863-.066-1.21l4.566-4.566ZM15.37 18.825c0-.756.913-1.134 1.447-.6l4.496 4.496c.344.344.33.91-.058 1.205a11.138 11.138 0 0 1-4.976 2.126c-.488.078-.91-.314-.91-.808v-6.42ZM10.634 15.664c.756 0 1.134.913.6 1.448l-4.56 4.56c-.348.348-.922.328-1.213-.069a11.133 11.133 0 0 1-2.046-5.044c-.067-.483.323-.895.81-.895h6.41ZM24.774 15.664c.488 0 .878.412.811.895a11.132 11.132 0 0 1-1.973 4.942c-.288.403-.866.426-1.217.075l-4.464-4.464c-.535-.535-.156-1.448.6-1.448h6.243ZM5.574 8.246c.294-.389.86-.403 1.205-.059l4.455 4.455c.534.534.156 1.447-.6 1.447H4.263c-.495 0-.888-.423-.808-.912a11.138 11.138 0 0 1 2.12-4.931ZM22.291 8.281c.347-.347.918-.33 1.21.065a11.135 11.135 0 0 1 2.044 4.831c.08.489-.313.912-.808.912H18.53c-.755 0-1.133-.913-.6-1.447l4.361-4.36ZM15.37 4.756c0-.494.42-.886.909-.808 1.784.285 3.427.99 4.824 2.013.398.291.417.865.069 1.213l-4.355 4.354c-.534.534-1.447.156-1.447-.6V4.757ZM12.897 3.921c.485-.07.898.321.898.81v6.198c0 .755-.914 1.133-1.448.6L7.924 7.104c-.35-.351-.328-.93.075-1.218a11.132 11.132 0 0 1 4.898-1.966Z"/></svg>'''
def _eoc(t):return 1-pow(1-t,3)
def _eob(t):return 1+2.70158*pow(t-1,3)+1.70158*pow(t-1,2)
def _svg(s,c):import io;return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=_S.format(c=c).encode(),output_width=s,output_height=s))).convert('RGBA')
def _fnt(s):
 for p in["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/TTF/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
  if os.path.exists(p):return ImageFont.truetype(p,s)
 return ImageFont.load_default()
def _frm(n,ic,bg,tc,dc,lc):
 im=Image.new('RGBA',(WIDTH,HEIGHT),bg+(255,));dr=ImageDraw.Draw(im);ls,lx,ly,to,tx,do,dr_=LOGO_BIG,WIDTH//2,HEIGHT//2,0,WIDTH+200,0,0
 if n<=30:p=1+.03*math.sin(n*.3);ls=int(LOGO_BIG*p)
 elif n<=60:e=_eoc((n-30)/30);ls=int(LOGO_BIG-(LOGO_BIG-LOGO_SMALL)*e);lx=int(WIDTH//2-(WIDTH//2-FINAL_LOGO_X)*e);ly=int(HEIGHT//2-(HEIGHT//2-FINAL_LOGO_Y)*e)
 elif n<=90:e=min(1,max(0,_eob((n-60)/30)));ls,lx,ly=LOGO_SMALL,FINAL_LOGO_X,FINAL_LOGO_Y;to=int(255*e);tx=int(WIDTH+200-(WIDTH+200-FINAL_TEXT_X)*e)
 else:ls,lx,ly,to,tx=LOGO_SMALL,FINAL_LOGO_X,FINAL_LOGO_Y,255,FINAL_TEXT_X;do=int(255*min(1,(n-90)/20));dr_=(n-90)*12
 if ls not in ic:ic[ls]=_svg(ls,lc)
 im.paste(ic[ls],(lx-ls//2,ly-ls//2),ic[ls])
 if to>0:dr.text((tx,FINAL_TEXT_Y),"LimeOS",font=_fnt(72),fill=tc+(to,))
 if do>0:
  cx,cy,r,dr2,nd=WIDTH//2,FINAL_DOTS_Y,25,6,8
  for i in range(nd):a=math.radians(i*45+dr_);dx,dy=int(cx+r*math.cos(a)),int(cy+r*math.sin(a));f=.3+.7*((nd-1-i)/(nd-1));dr.ellipse([dx-dr2,dy-dr2,dx+dr2,dy+dr2],fill=dc+(int(do*f),))
 return im.convert('RGB')
def _thm(o,f,bg):
 (o/"limeos.plymouth").write_text(f"[Plymouth Theme]\nName=LimeOS\nDescription=LimeOS animated boot splash\nModuleName=script\n\n[script]\nImageDir=/usr/share/plymouth/themes/limeos\nScriptFile=/usr/share/plymouth/themes/limeos/limeos.script\n")
 b=f"{bg[0]/255},{bg[1]/255},{bg[2]/255}";(o/"limeos.script").write_text(f"Window.SetBackgroundTopColor({b});Window.SetBackgroundBottomColor({b});frame_count={f+1};for(i=0;i<frame_count;i++){{frames[i]=Image(\"frame-\"+String(i).PadLeft(4,\"0\")+\".png\");}}current_frame=0;loop_start=91;sprite=Sprite();sprite.SetImage(frames[0]);sprite.SetX(Window.GetWidth()/2-frames[0].GetWidth()/2);sprite.SetY(Window.GetHeight()/2-frames[0].GetHeight()/2);fun refresh_callback(){{sprite.SetImage(frames[current_frame]);current_frame++;if(current_frame>=frame_count){{current_frame=loop_start;}}}}Plymouth.SetRefreshFunction(refresh_callback);fun progress_callback(duration,progress){{}}Plymouth.SetBootProgressFunction(progress_callback);")
def _gen(bg,tc,dc,lc,nm):
 o=_D/f"output-{nm}";o.mkdir(parents=True,exist_ok=True);[f.unlink()for f in o.glob("frame-*.png")]
 print(f"Generating {nm} theme: {o}");ic={}
 for n in range(TOTAL_FRAMES+1):print(f"\rFrame {n:4d}/{TOTAL_FRAMES}",end="",flush=True);_frm(n,ic,bg,tc,dc,lc).save(o/f"frame-{n:04d}.png","PNG")
 print("\nGenerating preview...");sp.run(["ffmpeg","-y","-framerate",str(FPS),"-i",str(o/"frame-%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-crf","18",str(o/"preview.mp4")],capture_output=True)
 _thm(o,TOTAL_FRAMES,bg);print(f"Done: {o}\n")
def main():
 print("LimeOS Plymouth Animation Generator\n"+"="*40)
 print(f"Resolution: {WIDTH}x{HEIGHT} | Frames: {TOTAL_FRAMES+1} | Duration: {(TOTAL_FRAMES+1)/FPS:.2f}s\n")
 _gen(BG_COLOR,TEXT_COLOR,DOT_COLOR,"#%02x%02x%02x"%TEXT_COLOR,"light")
 _gen(tuple(255-c for c in BG_COLOR),tuple(255-c for c in TEXT_COLOR),tuple(255-c for c in DOT_COLOR),"#%02x%02x%02x"%tuple(255-c for c in TEXT_COLOR),"dark")
 print("All themes generated!")
if __name__=="__main__":main()
