/** Selected unchanged paint definitions from Shapes.js; Copyright (c) 2006-2015 JGraph Holdings Ltd; Apache-2.0. */
(function(){
function CylinderShape3(bounds, fill, stroke, strokewidth)
	{
		mxShape.call(this);
		this.bounds = bounds;
		this.fill = fill;
		this.stroke = stroke;
		this.strokewidth = (strokewidth != null) ? strokewidth : 1;
	};
	
	mxUtils.extend(CylinderShape3, mxCylinder);

	CylinderShape3.prototype.size = 15;
	
	CylinderShape3.prototype.paintVertexShape = function(c, x, y, w, h)
	{
		var size = Math.max(0, Math.min(h * 0.5, parseFloat(mxUtils.getValue(this.style, 'size', this.size))));
		var lid = mxUtils.getValue(this.style, 'lid', true);

		c.translate(x,y);

		if (size == 0)
		{
			c.rect(0, 0, w, h);
			c.fillAndStroke();
		}
		else
		{
			c.begin();
			
			if (lid)
			{
				c.moveTo(0, size);
				c.arcTo(w * 0.5, size, 0, 0, 1, w * 0.5, 0);
				c.arcTo(w * 0.5, size, 0, 0, 1, w, size);
			}
			else
			{
				c.moveTo(0, 0);
				c.arcTo(w * 0.5, size, 0, 0, 0, w * 0.5, size);
				c.arcTo(w * 0.5, size, 0, 0, 0, w, 0);
			}

			c.lineTo(w, h - size);
			c.arcTo(w * 0.5, size, 0, 0, 1, w * 0.5, h);
			c.arcTo(w * 0.5, size, 0, 0, 1, 0, h - size);
			c.close();
			c.fillAndStroke();
			
			c.setShadow(false);
			
			if (lid)
			{
				c.begin();
				c.moveTo(w, size);
				c.arcTo(w * 0.5, size, 0, 0, 1, w * 0.5, 2 * size);
				c.arcTo(w * 0.5, size, 0, 0, 1, 0, size);
				c.stroke();
			}
		}
	};

	mxCellRenderer.registerShape('cylinder3', CylinderShape3);
function HexagonShape()
	{
		mxActor.call(this);
	};

	mxUtils.extend(HexagonShape, mxHexagon);

	HexagonShape.prototype.size = 0.25;

	HexagonShape.prototype.fixedSize = 20;

	HexagonShape.prototype.isRoundable = function()
	{
		return true;
	};
	HexagonShape.prototype.redrawPath = function(c, x, y, w, h)
	{
		var fixed = mxUtils.getValue(this.style, 'fixedSize', '0') != '0';
		var s = (fixed) ? Math.max(0, Math.min(w * 0.5, parseFloat(mxUtils.getValue(this.style, 'size', this.fixedSize)))) :
			w * Math.max(0, Math.min(1, parseFloat(mxUtils.getValue(this.style, 'size', this.size))));
		var arcSize = mxUtils.getValue(this.style, mxConstants.STYLE_ARCSIZE, mxConstants.LINE_ARCSIZE) / 2;
		this.addPoints(c, [new mxPoint(s, 0), new mxPoint(w - s, 0), new mxPoint(w, 0.5 * h), new mxPoint(w - s, h),
		                   new mxPoint(s, h), new mxPoint(0, 0.5 * h)], this.isRounded, arcSize, true);
	};

	mxCellRenderer.registerShape('hexagon', HexagonShape);
})();
