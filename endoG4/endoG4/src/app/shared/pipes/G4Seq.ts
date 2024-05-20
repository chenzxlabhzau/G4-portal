import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
@Pipe({
  name: 'G4Seq',
})
export class G4Seq implements PipeTransform {
  constructor(private sanitizer:DomSanitizer){}
  transform(seq: string, rl1:number,rl2:number,rl3:number,
            ll1:number,ll2:number,ll3:number, strand:string): unknown {
    let rl4 = seq.length - rl1-ll1-rl2-ll2-rl3-ll3
    let htmlString = '';
    let previousIndex = 0;
    if (strand=="+"){
      htmlString += `<span style='color:red'>${seq.substr(0,rl1)}</span>`;
      htmlString += seq.substr(rl1,ll1);
      htmlString += `<span style='color:red'>${seq.substr(rl1+ll1,rl2)}</span>`;
      htmlString += seq.substr(rl1+ll1+rl2,ll2);
      htmlString += `<span style='color:red'>${seq.substr(rl1+ll1+rl2+ll2,rl3)}</span>`;
      htmlString += seq.substr(rl1+ll1+rl2+ll2+rl3,ll3);
      htmlString += `<span style='color:red'>${seq.substr(rl1+ll1+rl2+ll2+rl3+ll3,rl4)}</span>`;
    }else {
      console.log(rl4)
      htmlString += `<span style='color:red'>${seq.substr(0,rl4)}</span>`;
      htmlString += seq.substr(rl4,ll3);
      htmlString += `<span style='color:red'>${seq.substr(rl4+ll3,rl3)}</span>`;
      htmlString += seq.substr(rl4+ll3+rl3,ll2);
      htmlString += `<span style='color:red'>${seq.substr(rl4+ll3+rl3+ll2,rl2)}</span>`;
      htmlString += seq.substr(rl4+ll3+rl3+ll2+rl2,ll1);
      htmlString += `<span style='color:red'>${seq.substr(rl4+ll3+rl3+ll2+rl2+ll1,rl1)}</span>`;
    }
    return this.sanitizer.bypassSecurityTrustHtml(htmlString)
  }
}
