import { Pipe } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

@Pipe({name: 'GID'})
export class GID {
  constructor(private sanitizer:DomSanitizer){}

  transform(gid:any,group) {
    if (group==null){
      let html = `<span>${gid}</span>`
      console.log("null")
      return this.sanitizer.bypassSecurityTrustHtml(html);
    }else {
      if (group.startsWith('Level')){
        let html = `<a href='#/detail/${gid}'>${gid}</a>`
        console.log("link")
        return this.sanitizer.bypassSecurityTrustHtml(html);
      }else {
        let html = `<span>${gid}</span>`
        console.log("nolevel")
        return this.sanitizer.bypassSecurityTrustHtml(html);
      }
    }

  }
}
