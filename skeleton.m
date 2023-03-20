numfiles = 499;

for k = 0:numfiles
  myfilename = sprintf('numero%d.png', k);
  A = imread(myfilename);
  B=im2gray(A);
  C = imbinarize(B);
  D = bwskel(C);
  name=sprintf('nuevo_numero%d.png', k);
  imwrite(D, name);
end


