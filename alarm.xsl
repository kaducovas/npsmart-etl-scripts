<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">

<xsl:output method="text"/>
<xsl:output method="text" indent="no" name="text"/>
<xsl:strip-space elements="*"/>
<xsl:param name="delimiter" select="';'"/>
<xsl:template match="/">

<xsl:for-each select="/ExportFileInfo/Record[1]/column">
	<xsl:value-of select="lower-case(@name)"/><xsl:if test="position() != last()">
		<xsl:value-of select="$delimiter"/>
	</xsl:if>
</xsl:for-each>
<xsl:text>&#xa;</xsl:text>
	<xsl:for-each select="/ExportFileInfo/Record">
	<xsl:for-each select="./column">
		<xsl:value-of select="."/>
		<xsl:if test="position() != last()">
			<xsl:value-of select="$delimiter"/>
		</xsl:if>
	</xsl:for-each>
	<xsl:text>&#xa;</xsl:text>
</xsl:for-each>

</xsl:template>
</xsl:stylesheet>