#ifndef EXTERN_API_H
#define EXTERN_API_H
#include "darknet.h"

network load_detect_model(char *cfgfile,char *weightsfil,int gpu_index );
box detect(char *filename,network * net,char *datacfg,float thresh,float hier_thresh,float nms,int use_opencv,int draw,int fullscreen);

#endif
