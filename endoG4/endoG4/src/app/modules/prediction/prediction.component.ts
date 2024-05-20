import { Component, OnInit } from '@angular/core';
import {  FileUploader,   } from 'ng2-file-upload';
import { environment } from '../../../environments/environment';
import { PredictionApiService } from './prediction-api.service';
import {catchError, tap} from "rxjs/operators";
import {of} from "rxjs";
@Component({
  selector: 'app-prediction',
  templateUrl: './prediction.component.html',
  styleUrls: ['./prediction.component.css']
})
export class PredictionComponent implements OnInit {
  assets = environment.assets;


  constructor(private DataApiService: PredictionApiService) {
  }
  seq_str=""
  uploading = false
  overlapping = 'False';
  max_length = 50
  se_lengths = Array.from(Array(60 - 10 + 1).keys()).map(x => x + 10)
  min_score = 50
  min_scores = Array.from(Array(70 - 20 + 1).keys()).map(x => x + 20)
  min_run = 2
  min_runs = [2,3,4,5]
  max_runs = [9,10,11,12,13,14,15]
  max_run = 11
  min_loop = 0
  min_loops = Array.from(Array(40 - 0 + 1).keys()).map(x => x + 0)
  max_loops = Array.from(Array(50 - 10 + 1).keys()).map(x => x + 10)
  max_loop = 30
  max_bulges = Array.from(Array(10 - 0 + 1).keys()).map(x => x + 0)
  max_bulge = 3
  max_mismatches = [0,1,2,3]
  max_mismatch = 3
  max_defects = Array.from(Array(10 - 0 + 1).keys()).map(x => x + 0)
  max_defect = 3
  ngOnInit(): void {
    this.uploader.onWhenAddingFileFailed = () => {
      alert("Maximun allowed file size is 1MB");
      this.uploader.clearQueue();
    }
    this.uploader.onAfterAddingFile = f => {
      if (this.uploader.queue.length > 1) {
        this.uploader.removeFromQueue(this.uploader.queue[0]);
      }
      f.withCredentials = false;
    };
  }


  public Analyze(): void{
    this.uploading = true
    if (this.uploader.queue.length==1){
      console.log(this.uploader.options.url)
      this.uploader.setOptions({url: environment.apiURL + "/prediction/upload?" + "overlapping=" + this.overlapping +
      "&max_length=" + this.max_length + "&min_score=" + this.min_score +
      "&max_bulge=" + this.max_bulge + "&max_mismatch=" + this.max_mismatch+
      "&max_defect=" + this.max_defect + "&min_loop=" + this.min_loop+
      "&max_loop=" + this.max_loop + "&min_run=" + this.min_run+ "&max_run=" + this.max_run})
      this.uploader.queue[0].upload()
      this.uploader.queue[0].onSuccess = (response, status, headers) => {
        this.uploading = false
      // 上传文件成功
        if (status == 200) {
          this.DataApiService.downloadFile(environment.Burl+"/static/prediction/upload/" + response.replace(/"/g,""),
            "EndoQuad_PQS.txt")
        }else {
            alert("Something wrong, please check your input file")
        }
      };
    }else {
      if (this.seq_str!=""){
        console.log(this.seq_str)
        // @ts-ignore
        // @ts-ignore
        this.DataApiService.pRecords(
          this.seq_str,
          this.overlapping,
          this.max_length,
          this.min_score,
          this.max_bulge,
          this.max_mismatch,
          this.max_defect,
          this.min_loop,
          this.max_loop,
          this.min_run,
          this.max_run,
        ).pipe(tap((val) => {
          this.uploading = false
          this.DataApiService.downloadFile(environment.Burl+"/static/prediction/upload/"  + val.replace(/"/g,""),
            "EndoQuad_PQS.txt")
        }),
          catchError(err => {

            this.uploading = false;
            alert("Something wrong, please check your input file");
            return of([])
          })
          ).subscribe()
      }else {
        this.uploading = false
      }
    }





  }

  public uploader:FileUploader = new FileUploader({
    isHTML5: true,
    method: "POST",  //上传方式
    itemAlias: "prediction_file",  //别名（后台接受参数名）
    autoUpload: false,  //是否自动上传（如果为true，则在input选择完后自动上传）
    maxFileSize : 1024 * 1024 * 1
  });
}
