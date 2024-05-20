import { Component, OnInit, Input, ViewChild, ElementRef } from '@angular/core';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-help',
  templateUrl: './help.component.html',
  styleUrls: ['./help.component.css']
})
export class HelpComponent implements OnInit {
  public assets = environment.assets;
  constructor() { }
  @ViewChild('canvasEl', { static: true }) canvasEl: ElementRef<HTMLCanvasElement>;
  private context: CanvasRenderingContext2D
  private drawEmail(email: string): void {
    this.context.font = '15px Arial';
    this.context.textBaseline = 'middle';
    this.context.textAlign = 'left';

    const x = 0;
    const y = (this.canvasEl.nativeElement as HTMLCanvasElement).height / 2;
    this.context.fillText('Email: ' + email, x, y);
  }
  ngOnInit(): void {
    this.context = (this.canvasEl.nativeElement as HTMLCanvasElement).getContext('2d');
    this.drawEmail("zhen-xia.chen@mail.hzau.edu.cn");
  }

}
