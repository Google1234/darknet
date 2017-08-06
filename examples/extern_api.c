#include "extern_api.h"

#include <time.h>
#include <stdlib.h>
#include <stdio.h>


network load_detect_model(char *cfgfile,char *weightsfile,int gpu_index)
//network load_detect_model(char *cfg,char *weights,int gpu_index =0)
/*
cfg:			net struct file
weightsfile:		model file 
gpu_index:		use which gpu 
*/
{ 
    if(gpu_index >= 0){
        cuda_set_device(gpu_index);
    }
    //only support run on single gpu
    network net = parse_network_cfg(cfgfile);
    if(weightsfile){
        load_weights(&net, weightsfile);
    }
    //only support run on single batch
    set_batch_network(&net, 1);

    return net;
}
box  detect(char *filename,network * _net,char *datacfg,float thresh,float hier_thresh,float nms,int use_opencv,int draw,int fullscreen)
//box  detect(char *filename,network &net,char *datacfg,float thresh=.24,float hier_thresh=.5,float nms=.3,int use_opencv,int draw=1,int fullscreen=1)
/*
filename:		image use for detect
net:			loaded net
datacfg:		dataset config file
thresh:			bigger than this->fg smaller->bg
hier_thresh:		used for tree label
nms:			non-maximum suppression
use_opencv:		show result or not
draw:			draw and save result or not
fullscreen:		show in full screen or not
*/
{
    network net=*_net;

    srand(2222222);
    double time;
    int j;
    time=what_time_is_it_now();
    //part 1 :load config
    list *options = read_data_cfg(datacfg);
    char *name_list = option_find_str(options, "names", "data/names.list");
    char **names = get_labels(name_list);
    image **alphabet = load_alphabet();

    image im = load_image_color(filename,0,0);
    image sized = letterbox_image(im, net.w, net.h);

    layer l = net.layers[net.n-1];

    box *boxes = calloc(l.w*l.h*l.n, sizeof(box));
    float **probs = calloc(l.w*l.h*l.n, sizeof(float *));
    for(j = 0; j < l.w*l.h*l.n; ++j) probs[j] = calloc(l.classes + 1, sizeof(float *));
    float **masks = 0;
    if (l.coords > 4){
        masks = calloc(l.w*l.h*l.n, sizeof(float*));
        for(j = 0; j < l.w*l.h*l.n; ++j) masks[j] = calloc(l.coords-4, sizeof(float *));
    }

    float *X = sized.data;
    network_predict(net, X);
    get_region_boxes(l, im.w, im.h, net.w, net.h, thresh, probs, boxes, masks, 0, 0, hier_thresh, 1);
    if (nms) do_nms_obj(boxes, probs, l.w*l.h*l.n, l.classes, nms);
    //else if (nms) do_nms_sort(boxes, probs, l.w*l.h*l.n, l.classes, nms);

     printf("%s: Predicted in %f seconds.\n", filename, what_time_is_it_now()-time);

     if (draw)
     {
        draw_detections(im, l.w*l.h*l.n, thresh, boxes, probs, masks, names, alphabet, l.classes);
        save_image(im, "predictions");
     }
     if (use_opencv)
     {
        cvNamedWindow("predictions", CV_WINDOW_NORMAL);
        if(fullscreen){
            cvSetWindowProperty("predictions", CV_WND_PROP_FULLSCREEN, CV_WINDOW_FULLSCREEN);
        }
        show_image(im, "predictions");
        cvWaitKey(0);
        cvDestroyAllWindows();
     }

    free_image(im);
    free_image(sized);
    //free(boxes);
    free_ptrs((void **)probs, l.w*l.h*l.n);

    return *boxes;
}

int test_main(int argc, char **argv)
{
    network net=load_detect_model("/home/jtao/jto/code/darknet/cfg/tt100k_test.cfg","/home/jtao/jto/code/darknet/backup/tt100k_small_input_and_voc_anchors/tt100k.backup",0);
    box detect_box=detect("/home/jtao/jto/code/darknet/data/dataset/tt100k/JPEGImages/64398.jpg",&net,"/home/jtao/jto/code/darknet/cfg/tt100k.data",0.1,0.5,0.3,0,1,0);
    return 1;
}
