import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
@Pipe({
  name: 'GeneUrl',
})
export class GeneUrl implements PipeTransform {
  private sp: any;
  constructor(private sanitizer:DomSanitizer){}
  transform(value: string, ...args: unknown[]): unknown {
    if (value.startsWith("ENSGA")){
    if (value.indexOf(",")!=-1){
      let aa = `<a href="https://www.ensembl.org/Gallus_gallus_GCA_000002315.5/Gene/Idhistory?g=${value.split(", ")[0]}" target="_blank">${value.split(", ")[0]}</a></a>, <a href="http://www.ensembl.org/Gallus_gallus_GCA_000002315.5/Gene/Idhistory?g=${value.split(", ")[1]}" target="_blank">${value.split(", ")[1]}</a></a>`;
      return this.sanitizer.bypassSecurityTrustHtml(aa)
    }else {
      let aa = `<a href="https://www.ensembl.org/Gallus_gallus_GCA_000002315.5/Gene/Idhistory?g=${value}" target="_blank">${value}</a></a>`
      return this.sanitizer.bypassSecurityTrustHtml(aa)
    }
    }
    if (value.startsWith("ENSMUSG")){
      this.sp = "Mus_musculus"
    }
    if (value.startsWith("ENSG")){
      this.sp = "Homo_sapiens"
    }
    if (value.startsWith("WBGene")){
      this.sp = "Caenorhabditis_elegans"
    }
    if (value.startsWith("FBgn")){
      this.sp = "Drosophila_melanogaster"
    }
    if (value.startsWith("ENSMOD")){
      this.sp = "Monodelphis_domestica"
    }
    if (value.startsWith("ENSSSCG")){
      this.sp = "Sus_scrofa"
    }
    if (value.startsWith("ENSOCUG")){
      this.sp = "Oryctolagus_cuniculus"
    }
    if (value.startsWith("ENSRNOG")){
      this.sp = "Rattus_norvegicus"
    }
    if (value.startsWith("ENSMMUG")){
      this.sp = "Macaca_mulatta"
    }
    if (value.startsWith("ENSDARG")){
      this.sp = "Danio_rerio"
    }
    if (value.indexOf(",")!=-1){
      let aa = `<a href="https://www.ensembl.org/${this.sp}/Gene/Summary?db=core;g=${value.split(", ")[0]}" target="_blank">${value.split(", ")[0]}</a></a>, <a href="http://www.ensembl.org/${this.sp}/Gene/Summary?db=core;g=${value.split(", ")[1]}" target="_blank">${value.split(", ")[1]}</a></a>`;
      return this.sanitizer.bypassSecurityTrustHtml(aa)
    }else {
      let aa = `<a href="https://www.ensembl.org/${this.sp}/Gene/Summary?db=core;g=${value}" target="_blank">${value}</a></a>`
      return this.sanitizer.bypassSecurityTrustHtml(aa)
    }
  }
}
